"""Conservative 3MF package inspector; never extracts or follows external links."""
import hashlib
import io
import json
import math
import posixpath
import re
import stat
import struct
import xml.etree.ElementTree as ET
import zipfile
import zlib

CORE = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
START = 'http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel'
MAX_ENTRIES = 128
MAX_MEMBER = 8 * 1024 * 1024
MAX_TOTAL = 32 * 1024 * 1024
MAX_RATIO = 200
MAX_OBJECTS = 256
MAX_REFERENCES = 2048
MAX_NODES = 200000


class Invalid3MF(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid3MF(message)


class BoundedTree(ET.TreeBuilder):
    def __init__(self):
        super().__init__()
        self.nodes = self.depth = 0

    def start(self, tag, attrs):
        self.nodes += 1
        self.depth += 1
        require(self.nodes <= MAX_NODES and self.depth <= 64, 'XML node/depth limit exceeded.')
        require(len(tag) <= 1024 and len(attrs) <= 32, 'XML tag/attribute limit exceeded.')
        require(all(len(k) <= 1024 and len(v) <= 1024 for k, v in attrs.items()), 'XML attribute length limit exceeded.')
        return super().start(tag, attrs)

    def end(self, tag):
        self.depth -= 1
        return super().end(tag)

    def doctype(self, *args):
        raise Invalid3MF('DTD declarations are forbidden.')


def xml(data):
    try:
        text = data.decode('utf-8-sig')
        require('\x00' not in text, 'XML must be UTF-8.')
        require(not re.search(r'<!\s*(DOCTYPE|ENTITY)', text, re.I), 'DTD/entity declarations are forbidden.')
        declaration = re.match(r'<\?xml\s+[^?]*encoding\s*=\s*[\'"]([^\'"]+)', text, re.I)
        require(not declaration or declaration.group(1).lower() == 'utf-8', 'XML encoding must be UTF-8.')
        return ET.fromstring(text, parser=ET.XMLParser(target=BoundedTree()))
    except (UnicodeError, ET.ParseError) as exc:
        raise Invalid3MF('Malformed or unsupported XML: ' + str(exc)) from exc


def name_safe(name):
    require(0 < len(name) <= 512, 'ZIP member name length limit exceeded.')
    require(not any(ord(c) < 32 for c in name) and not any(c in name for c in '\\:%?#'), 'Unsafe/unsupported ZIP member name.')
    require(not name.startswith('/') and all(p not in ('', '.', '..') for p in name.rstrip('/').split('/')), 'Unsafe ZIP member path.')


def number(value):
    require(value is not None and len(value) <= 128, 'Missing/oversized numeric value.')
    value = value.strip(' \t\r\n')  # XML Schema numeric whitespace, not arbitrary Unicode whitespace.
    require(re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?', value) is not None, 'Invalid numeric syntax.')
    try:
        result = float(value)
    except ValueError as exc:
        raise Invalid3MF('Invalid numeric value.') from exc
    require(math.isfinite(result), 'Nonfinite numeric value.')
    return result


def integer(value, minimum=0):
    if value is not None:
        value = value.strip(' \t\r\n')
    require(value is not None and re.fullmatch(r'[0-9]{1,10}', value) is not None, 'Invalid integer reference.')
    result = int(value)
    require(minimum <= result <= 2147483647, 'Integer reference out of range.')
    return result


def transform(node):
    literal = node.get('transform')
    if literal is None:
        return {'status': 'identity_default', 'literal': None}
    tokens = literal.split()
    require(len(tokens) == 12, 'Transform must contain 12 finite numbers.')
    for token in tokens:
        number(token)
    return {'status': 'finite_values_checked_not_applied', 'literal': literal}


def inspect_3mf(data):
    try:
        return _inspect(data)
    except (zipfile.BadZipFile, zlib.error, UnicodeError, RuntimeError, NotImplementedError, EOFError, OSError) as exc:
        raise Invalid3MF('Invalid or unsupported ZIP: ' + str(exc)) from exc


def _inspect(data):
    # Bound central-directory object allocation before invoking ZipFile, including ZIP64 metadata.
    eocd = data.rfind(b'PK\x05\x06', max(0, len(data) - 65557))
    require(eocd >= 0 and eocd + 22 <= len(data), 'Missing ZIP end record.')
    disk, central_disk, on_disk, entries, size, offset, comment = struct.unpack_from('<4H2IH', data, eocd + 4)
    require(eocd + 22 + comment == len(data), 'Trailing or malformed ZIP end record.')
    require(disk == central_disk == 0 and on_disk == entries, 'Multipart ZIP unsupported.')
    directory_end = eocd
    has_locator = eocd >= 20 and data[eocd-20:eocd-16] == b'PK\x06\x07'
    if has_locator:
        loc_disk, zip64_offset, disks = struct.unpack_from('<IQI', data, eocd-16)
        require(loc_disk == 0 and disks == 1, 'Multipart ZIP64 unsupported.')
        require(zip64_offset + 56 == eocd - 20 and data[zip64_offset:zip64_offset+4] == b'PK\x06\x06', 'Unsupported ZIP64 end record layout.')
        record_size, made, needed, zdisk, zcentral_disk, zon_disk, zentries, zsize, zoffset = struct.unpack_from('<Q2H2I4Q', data, zip64_offset + 4)
        require(record_size == 44 and zdisk == zcentral_disk == 0 and zon_disk == zentries, 'Invalid ZIP64 end record.')
        require(entries in (65535, zentries) and on_disk in (65535, zon_disk) and size in (0xffffffff, zsize) and offset in (0xffffffff, zoffset), 'Inconsistent ZIP64 metadata.')
        entries, size, offset = zentries, zsize, zoffset
        directory_end = zip64_offset
    require(entries <= MAX_ENTRIES and size != 0xffffffff and offset != 0xffffffff, 'ZIP entry limit or missing ZIP64 metadata.')
    require(offset + size == directory_end, 'Unsupported ZIP directory layout.')
    cursor, actual_entries = offset, 0
    while cursor < directory_end:
        require(cursor + 46 <= directory_end and data[cursor:cursor+4] == b'PK\x01\x02', 'Malformed central directory.')
        lengths = struct.unpack_from('<3H', data, cursor + 28)
        cursor += 46 + sum(lengths)
        actual_entries += 1
        require(actual_entries <= MAX_ENTRIES and cursor <= directory_end, 'ZIP central directory entry limit exceeded.')
    require(actual_entries == entries, 'Inconsistent ZIP entry count.')
    inventory, profiles, trees = [], [], {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        require(len(infos) == entries, 'Inconsistent ZIP entry count.')
        names, total = set(), 0
        for info in infos:
            name = info.filename
            name_safe(name)
            require(info.orig_filename == name, 'NUL in ZIP member name.')
            require(name.casefold() not in names, 'Duplicate ZIP member name.')
            names.add(name.casefold())
            require(not info.flag_bits & 1, 'Encrypted ZIP unsupported.')
            require(info.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED), 'Unsupported ZIP compression.')
            mode = info.external_attr >> 16
            require(not stat.S_ISLNK(mode), 'ZIP symlink unsupported.')
            total += info.file_size
            require(info.file_size <= MAX_MEMBER and total <= MAX_TOTAL, 'ZIP expanded size limit exceeded.')
            require(info.file_size <= MAX_RATIO * max(1, info.compress_size), 'ZIP compression ratio limit exceeded.')
        members = {info.filename: info for info in infos if not info.is_dir()}
        for name in sorted(members):
            info = members[name]
            with archive.open(info) as source:
                payload = source.read(MAX_MEMBER + 1)
            require(len(payload) == info.file_size and len(payload) <= MAX_MEMBER, 'ZIP member size mismatch.')
            item = {'path': name, 'byte_size': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()}
            inventory.append(item)
            if name.lower().endswith(('.xml', '.rels', '.model')) or name == '[Content_Types].xml':
                trees[name] = xml(payload)
            if name.lower().endswith(('.config', '.ini', '.json')) or any(t in name.lower() for t in ('profile', 'printticket')):
                profiles.append(dict(item, status='candidate_by_filename_only'))
        require('_rels/.rels' in trees and '[Content_Types].xml' in trees, 'Required package relationship/content-types part missing.')
        require(trees['[Content_Types].xml'].tag == '{http://schemas.openxmlformats.org/package/2006/content-types}Types', 'Wrong content-types namespace.')
        starts = []
        for path, tree in trees.items():
            if not path.endswith('.rels'):
                continue
            require(tree.tag == '{' + REL + '}Relationships', 'Wrong relationship namespace.')
            if path == '_rels/.rels':
                base = ''
            else:
                directory, filename = posixpath.split(path)
                require(posixpath.basename(directory) == '_rels', 'Unsupported relationship part path.')
                base = posixpath.dirname(directory)
                require(posixpath.join(base, filename[:-5]) in members, 'Relationship source missing.')
            ids = set()
            for rel in tree:
                require(rel.tag == '{' + REL + '}Relationship', 'Unexpected relationship element.')
                rid, target = rel.get('Id'), rel.get('Target')
                require(rid and rid not in ids, 'Missing/duplicate relationship ID.')
                ids.add(rid)
                require(rel.get('TargetMode', 'Internal') == 'Internal', 'External relationship unsupported; never fetched.')
                require(target and not any(c in target for c in '\\:%?#') and not target.startswith('//'), 'Unsafe relationship target.')
                target_path = posixpath.normpath(target.lstrip('/') if target.startswith('/') else posixpath.join(base, target))
                name_safe(target_path)
                require(target_path in members, 'Relationship target missing.')
                if path == '_rels/.rels' and rel.get('Type') == START:
                    starts.append(target_path)
        require(len(starts) == 1, 'Exactly one package StartPart relationship required.')
        model_path = starts[0]
        require(model_path in trees, 'Root model XML path has unsupported extension.')
        model = trees[model_path]
        result = model_summary(model, members)
        result.update(root_model_path=model_path, inventory=inventory, profile_candidates=profiles,
                      inventory_status='bounded_members_hashed', status='partial',
                      world_bounds={'status': 'not_computed'},
                      limits={'max_entries': MAX_ENTRIES, 'max_member_bytes': MAX_MEMBER, 'max_total_expanded_bytes': MAX_TOTAL, 'max_compression_ratio': MAX_RATIO})
        if sum(name.endswith('.model') for name in members) > 1:
            result['gaps'].append('Other model parts are XML-checked only; cross-part composition is unsupported.')
        require(len(json.dumps(result)) <= 1024 * 1024, 'Inspection output size limit exceeded.')
        return result


def model_summary(model, members):
    q = lambda tag: '{' + CORE + '}' + tag
    require(model.tag == q('model'), 'Root model has unsupported core namespace.')
    unit = model.get('unit', 'millimeter')
    require(unit in ('micron', 'millimeter', 'centimeter', 'inch', 'foot', 'meter'), 'Invalid core unit.')
    resources, builds = model.findall(q('resources')), model.findall(q('build'))
    require(len(resources) == len(builds) == 1, 'Exactly one resources and build element required.')
    resources, build = resources[0], builds[0]
    nodes = resources.findall(q('object'))
    require(0 < len(nodes) <= MAX_OBJECTS, 'Object count outside supported limit.')
    ids = {}
    for node in resources:
        if node.get('id') is not None:
            rid = integer(node.get('id'), 1)
            require(rid not in ids, 'Duplicate resource ID.')
            ids[rid] = node
    objects, refs, edges = [], [], {}
    gaps = ['Partial core inspection, not XSD or OPC conformance validation.',
            'No topology, physical dimensions in world space, materials, slicer settings, toolpaths, or production-readiness validation.']
    namespaces = set()
    for node in model.iter():
        for tag in [node.tag] + list(node.attrib):
            if tag.startswith('{'):
                ns = tag[1:].split('}')[0]
                if ns not in (CORE, 'http://www.w3.org/XML/1998/namespace'):
                    namespaces.add(ns)
    require(len(namespaces) <= 32, 'Extension namespace count limit exceeded.')
    if namespaces or model.get('requiredextensions'):
        gaps.append('Extension semantics unsupported, including any required extensions; do not manufacture from this inspection.')
    for node in nodes:
        oid = integer(node.get('id'), 1)
        meshes, comps = node.findall(q('mesh')), node.findall(q('components'))
        require(len(meshes) + len(comps) == 1, 'Object must have exactly one mesh or components group.')
        obj = {'id': oid, 'type': node.get('type', 'model')}
        edges[oid] = []
        if meshes:
            mesh = meshes[0]
            vs, ts = mesh.findall(q('vertices')), mesh.findall(q('triangles'))
            require(len(vs) == len(ts) == 1, 'Mesh requires vertices and triangles.')
            vertices, triangles = vs[0].findall(q('vertex')), ts[0].findall(q('triangle'))
            require(vertices and triangles, 'Mesh is empty.')
            for vertex in vertices:
                for axis in ('x', 'y', 'z'):
                    number(vertex.get(axis))
            for triangle in triangles:
                for key in ('v1', 'v2', 'v3'):
                    require(integer(triangle.get(key)) < len(vertices), 'Triangle vertex index out of range.')
            obj.update(kind='mesh', vertex_count=len(vertices), triangle_count=len(triangles), index_status='in_range')
        else:
            obj.update(kind='components', components=[])
            for component in comps[0].findall(q('component')):
                target = integer(component.get('objectid'), 1)
                item = {'objectid': target, 'transform': transform(component)}
                external_path = next((v for k, v in component.attrib.items() if k.startswith('{') and k.endswith('}path')), None)
                if external_path is not None:
                    require(external_path.startswith('/') and not external_path.startswith('//'), 'Unsupported cross-part path.')
                    name_safe(external_path[1:])
                    require(external_path[1:] in members, 'Cross-part model path missing.')
                    item.update(reference_status='unsupported_cross_part', path=external_path)
                else:
                    refs.append(target)
                    edges[oid].append(target)
                    item['reference_status'] = 'local_checked'
                obj['components'].append(item)
                require(sum(len(o.get('components', [])) for o in objects) + len(obj['components']) <= MAX_REFERENCES, 'Component limit exceeded.')
            require(obj['components'], 'Components group is empty.')
        objects.append(obj)
    if any(c.get('reference_status') == 'unsupported_cross_part' for obj in objects for c in obj.get('components', [])):
        gaps.append('Cross-part component paths exist, but referenced object IDs and transforms in other model parts are not verified.')
    items = []
    for item in build.findall(q('item')):
        target = integer(item.get('objectid'), 1)
        summary = {'objectid': target, 'transform': transform(item)}
        external_path = next((v for k, v in item.attrib.items() if k.startswith('{') and k.endswith('}path')), None)
        if external_path is not None:
            require(external_path.startswith('/') and not external_path.startswith('//'), 'Unsupported cross-part build path.')
            name_safe(external_path[1:])
            require(external_path[1:] in members, 'Cross-part build model path missing.')
            summary.update(reference_status='unsupported_cross_part', path=external_path)
            if not any('Cross-part build' in gap for gap in gaps):
                gaps.append('Cross-part build paths exist, but referenced object IDs and assembly semantics are not verified.')
        else:
            refs.append(target)
            summary['reference_status'] = 'local_checked'
        items.append(summary)
        require(len(items) <= MAX_REFERENCES, 'Build item limit exceeded.')
    object_ids = {obj['id'] for obj in objects}
    require(all(ref in object_ids for ref in refs), 'Missing object reference.')
    # Bounded iterative traversal detects nested cycles without recursion.
    for origin in edges:
        todo = [(origin, frozenset())]
        visited = set()
        while todo:
            current, trail = todo.pop()
            require(current not in trail, 'Component reference cycle.')
            if current in visited:
                continue
            visited.add(current)
            todo.extend((child, trail | {current}) for child in edges[current])
    return {'units': unit, 'units_source': 'model_attribute' if 'unit' in model.attrib else 'core_default',
            'object_count': len(objects), 'objects': objects, 'build_items': items,
            'extension_namespaces': sorted(namespaces), 'required_extensions_literal': model.get('requiredextensions'), 'gaps': gaps}

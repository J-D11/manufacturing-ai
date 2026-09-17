import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'inspect_asset.py'
CORE = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
START = 'http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel'
MESH = '<object id="1"><mesh><vertices><vertex x="0" y="0" z="0"/><vertex x="1" y="0" z="0"/><vertex x="0" y="1" z="0"/></vertices><triangles><triangle v1="0" v2="1" v3="2"/></triangles></mesh></object>'


def model(objects=MESH, attrs='', build='<item objectid="1"/>'):
    return ('<model xmlns="'+CORE+'" '+attrs+'><resources>'+objects+'</resources><build>'+build+'</build></model>').encode()


def package(payload=None, root='3D/custom.model', extras=(), target=None):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr('_rels/.rels', '<Relationships xmlns="'+REL+'"><Relationship Id="root" Type="'+START+'" Target="'+(target or '/'+root)+'"/></Relationships>')
        z.writestr(root, payload if payload is not None else model())
        for name, content in extras:
            z.writestr(name, content)
    return stream.getvalue()


class ThreeMFTests(unittest.TestCase):
    def invoke(self, data, extra=()):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'asset.3mf'
            path.write_bytes(data)
            process = subprocess.run([sys.executable, str(SCRIPT), str(path), *extra], capture_output=True, text=True, timeout=10)
            self.assertEqual(process.stderr, '')
            self.assertEqual(path.read_bytes(), data)
            return process.returncode, json.loads(process.stdout)

    def test_root_relationship_default_units_and_profile_hash(self):
        code, r = self.invoke(package(root='Elsewhere/actual.model', extras=[('Metadata/profile.json', b'{"temperature": 123}')]))
        self.assertEqual(code, 3)
        self.assertEqual(r['status'], 'partial')
        self.assertEqual(r['units'], 'millimeter')
        self.assertEqual(r['units_source'], 'core_default')
        g = r['geometry']
        self.assertEqual(g['root_model_path'], 'Elsewhere/actual.model')
        self.assertEqual(g['objects'][0]['triangle_count'], 1)
        self.assertEqual(g['profile_candidates'][0]['sha256'], hashlib.sha256(b'{"temperature": 123}').hexdigest())
        self.assertEqual(g['world_bounds']['status'], 'not_computed')
        self.assertNotIn('temperature', g['profile_candidates'][0])

    def test_explicit_units_and_nested_transforms_retained(self):
        literal = '1 0 0 0 1 0 0 0 1 10.00 20 30'
        objects = MESH + '<object id="2"><components><component objectid="1" transform="'+literal+'"/></components></object><object id="3"><components><component objectid="2"/></components></object>'
        code, r = self.invoke(package(model(objects, 'unit="inch"', '<item objectid="3" transform="'+literal+'"/>')))
        self.assertEqual(code, 3)
        self.assertEqual(r['units'], 'inch')
        self.assertEqual(r['geometry']['object_count'], 3)
        self.assertEqual(r['geometry']['objects'][1]['components'][0]['transform']['literal'], literal)
        self.assertEqual(r['geometry']['build_items'][0]['transform']['literal'], literal)
        self.assertEqual(self.invoke(package(), ['--units','mm'])[0], 2)

    def test_numeric_xml_whitespace_preserves_coordinate_and_reference_meaning(self):
        objects = MESH.replace('x="0"', 'x=" &#x9;0&#xA; "').replace('id="1"', 'id=" 1 "').replace('v3="2"', 'v3=" &#xD;2 "')
        objects += '<object id=" 2 "><components><component objectid=" 1 "/></components></object>'
        code, report = self.invoke(package(model(objects, build='<item objectid=" 2 "/>')))
        self.assertEqual(code, 3)
        self.assertEqual([o['id'] for o in report['geometry']['objects']], [1, 2])
        self.assertEqual(report['geometry']['objects'][0]['vertex_count'], 3)
        self.assertEqual(report['geometry']['build_items'][0]['objectid'], 2)
        self.assertEqual(report['geometry']['objects'][1]['components'][0]['objectid'], 1)

    def test_numeric_whitespace_does_not_accept_split_values_or_unicode_spaces(self):
        for value in ['1 2', '&#160;1', '1&#160;']:
            with self.subTest(value=value):
                self.assertEqual(self.invoke(package(model(MESH.replace('x="1"', 'x="'+value+'"'))))[0], 2)
                self.assertEqual(self.invoke(package(model(MESH.replace('id="1"', 'id="'+value+'"'))))[0], 2)

    def test_invalid_core_and_references_fail(self):
        cases = [model(attrs='unit="mm"'), model(MESH.replace('v3="2"','v3="9"')),
                 model(MESH.replace('x="1"','x="NaN"')), model(build='<item objectid="8"/>'),
                 model(MESH+MESH), model(build='<item objectid="1" transform="1 0 0"/>'),
                 model(build='<item objectid="1" transform="1 0 0 0 1 0 0 0 1 inf 0 0"/>'),
                 model('<object id="1"><components><component objectid="1"/></components></object>'),
                 model('<object id="1"><components><component objectid="7"/></components></object>')]
        for payload in cases:
            with self.subTest(payload=payload):
                code, r = self.invoke(package(payload))
                self.assertEqual(code, 2)
                self.assertEqual(r['geometry']['status'], 'not_verified')

    def test_unsafe_xml_rejected(self):
        for payload in [b'<!DOCTYPE model [<!ENTITY boom "x">]>'+model(), b'<model>', model().decode().encode('utf-16'), b'<?xml version="1.0" encoding="ISO-8859-1"?>'+model(), b'<!DOCTYPE model SYSTEM "https://example.invalid/x">'+model()]:
            with self.subTest(payload=payload[:30]):
                self.assertEqual(self.invoke(package(payload))[0], 2)

    def test_zip_limits_bad_names_and_missing_root(self):
        for data in [b'not zip', package(target='/missing.model'), package(target='https://example.invalid/model'),
                     package(extras=[('../escape', b'x')]), package(extras=[('/absolute', b'x')]),
                     package(extras=[('Metadata/bomb.txt', b'0'*100000)]),
                     package(extras=[('file'+str(i), b'x') for i in range(130)]),
                     package(extras=[('Metadata/large.bin', b'x'*(8*1024*1024+1))])]:
            with self.subTest(size=len(data)):
                self.assertEqual(self.invoke(data)[0], 2)

    def test_bounded_zip64_openscad_export_and_bad_metadata(self):
        import struct
        data = (Path(__file__).parent/'fixtures'/'openscad-enclosure-box.3mf').read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), '156096397311f660ddeea36d4b363d106c37e4be0e833d0240bb66a97843fa65')
        code, report = self.invoke(data)
        self.assertEqual(code, 3)
        self.assertEqual(report['geometry']['objects'][0]['triangle_count'], 28)
        self.assertEqual(report['units'], 'millimeter')
        for field, value in [(24, 129), (32, 129), (48, 999999999)]:
            bad = bytearray(data)
            end = bad.rfind(b'PK\x06\x06')
            struct.pack_into('<Q', bad, end + field, value)
            code, report = self.invoke(bytes(bad))
            self.assertEqual(code, 2)
            self.assertEqual(report['schema_version'], 2)
            self.assertEqual(report['units_source'], 'not_verified')
            self.assertFalse(any('STL' in limit for limit in report['limitations']))

    def test_corrupt_deflate_returns_structured_error(self):
        import struct
        data = bytearray(package())
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            info = archive.getinfo('3D/custom.model')
            offset = info.header_offset
            namesize, extrasize = struct.unpack_from('<HH', data, offset + 26)
            start = offset + 30 + namesize + extrasize
            data[start:start+info.compress_size] = b'\xff' * info.compress_size
        code, report = self.invoke(bytes(data))
        self.assertEqual(code, 2)
        self.assertEqual(report['status'], 'error')
        self.assertIn('ZIP', report['error'])

    def test_invalid_utf8_member_name_returns_structured_error(self):
        import struct
        data = bytearray(package())
        local = data.index(b'PK\x03\x04')
        central = data.index(b'PK\x01\x02')
        struct.pack_into('<H', data, local + 6, 0x800)
        struct.pack_into('<H', data, central + 8, 0x800)
        data[local + 30] = 0xff
        data[central + 46] = 0xff
        code, report = self.invoke(bytes(data))
        self.assertEqual(code, 2)
        self.assertEqual(report['geometry']['status'], 'not_verified')
        self.assertIn('error', report)

    def test_duplicate_members_rejected(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            data = package(extras=[('3D/custom.model', model())])
        self.assertEqual(self.invoke(data)[0], 2)

    def test_external_missing_and_ambiguous_relationships(self):
        for rels in [
            '<Relationship Id="r" Type="'+START+'" Target="/3D/custom.model" TargetMode="External"/>',
            '<Relationship Id="r" Type="'+START+'" Target="/3D/custom.model"/><Relationship Id="s" Type="'+START+'" Target="/3D/custom.model"/>',
            '<Relationship Id="r" Type="other" Target="/missing.png"/>']:
            stream = io.BytesIO(package())
            with zipfile.ZipFile(stream) as z:
                existing = [(i.filename,z.read(i)) for i in z.infolist() if i.filename != '_rels/.rels']
            out = io.BytesIO()
            with zipfile.ZipFile(out,'w') as z:
                for name, data in existing:
                    z.writestr(name,data)
                z.writestr('_rels/.rels','<Relationships xmlns="'+REL+'">'+rels+'</Relationships>')
            self.assertEqual(self.invoke(out.getvalue())[0], 2)

    def test_forged_zip_count_rejected_before_directory_allocation(self):
        import struct
        data = bytearray(package())
        end = data.rfind(b'PK\x05\x06')
        struct.pack_into('<HH', data, end + 8, 1, 1)
        self.assertEqual(self.invoke(bytes(data))[0], 2)

    def test_missing_cross_part_target_is_rejected(self):
        objects = '<object id="1"><components><component objectid="8" p:path="/missing.model"/></components></object>'
        self.assertEqual(self.invoke(package(model(objects, 'xmlns:p="https://vendor.invalid/production"')))[0], 2)

    def test_cross_part_build_is_not_claimed_as_local(self):
        attrs = 'xmlns:p="https://vendor.invalid/production"'
        payload = model(attrs=attrs, build='<item objectid="999" p:path="/3D/other.model"/>')
        code, result = self.invoke(package(payload, extras=[('3D/other.model', model())]))
        self.assertEqual(code, 3)
        item = result['geometry']['build_items'][0]
        self.assertEqual(item['reference_status'], 'unsupported_cross_part')
        self.assertEqual(item['path'], '/3D/other.model')
        self.assertTrue(any('Cross-part build' in gap for gap in result['geometry']['gaps']))
        self.assertEqual(self.invoke(package(payload))[0], 2)
        for target in ['https://invalid/model', '//3D/other.model', '/3D/%6fther.model']:
            with self.subTest(target=target):
                bad = model(attrs=attrs, build='<item objectid="999" p:path="'+target+'"/>')
                self.assertEqual(self.invoke(package(bad))[0], 2)

    def test_extensions_remain_explicit_gap(self):
        code, r = self.invoke(package(model(attrs='xmlns:x="https://vendor.invalid/ext" requiredextensions="x" x:flag="yes"')))
        self.assertEqual(code, 3)
        self.assertIn('https://vendor.invalid/ext', r['geometry']['extension_namespaces'])
        self.assertTrue(any('Extension semantics unsupported' in g for g in r['geometry']['gaps']))


if __name__ == '__main__':
    unittest.main()

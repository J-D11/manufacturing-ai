#!/usr/bin/env python3
"""Bounded, read-only fingerprints, STL inspection, and partial 3MF inspection."""
import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import stat
import struct
import sys
from inspect_3mf import inspect_3mf, Invalid3MF

MAX_BYTES = 64 * 1024 * 1024
MAX_ASCII_LINE_BYTES = 4096
LIMITATIONS = [
    'No topology, watertightness, self-intersection, wall-thickness, repair, or manufacturability checks.',
    'STL has no authoritative units; supplied units are a user assertion, not detected or converted.',
    'Degeneracy is a floating-point zero-area check; near-degenerate triangles may be missed.',
    'Normals are checked for finite values only; orientation and normal consistency are not verified.',
    'Inspection describes the captured bytes, not a future version or a machine job.',
]


class InvalidAsset(ValueError):
    pass


def numbers(tokens):
    if len(tokens) != 3:
        raise InvalidAsset('Expected exactly three coordinates.')
    try:
        values = tuple(float(token) for token in tokens)
    except ValueError as exc:
        raise InvalidAsset('Invalid numeric value.') from exc
    if not all(math.isfinite(value) for value in values):
        raise InvalidAsset('Nonfinite coordinate or normal.')
    return values


def ascii_triangles(data):
    def decoded_lines():
        source = io.BytesIO(data)
        while True:
            raw_line = source.readline(MAX_ASCII_LINE_BYTES + 1)
            if not raw_line:
                return
            if len(raw_line) > MAX_ASCII_LINE_BYTES:
                raise InvalidAsset('ASCII STL line exceeds the 4096-byte limit.')
            try:
                yield raw_line.decode('ascii')
            except UnicodeDecodeError as exc:
                raise InvalidAsset('Not an exact-length binary STL or supported ASCII STL.') from exc

    lines = decoded_lines()

    def line():
        for value in lines:
            value = value.strip()
            if value:
                return value.split()
        raise InvalidAsset('Truncated ASCII STL.')

    if line()[0] != 'solid':
        raise InvalidAsset('ASCII STL must begin with solid.')
    while True:
        tokens = line()
        if tokens[0] == 'endsolid':
            if any(value.strip() for value in lines):
                raise InvalidAsset('Trailing data or multiple solids are unsupported.')
            return
        if tokens[:2] != ['facet', 'normal']:
            raise InvalidAsset('Expected facet normal.')
        numbers(tokens[2:])
        if line() != ['outer', 'loop']:
            raise InvalidAsset('Expected outer loop.')
        vertices = []
        for _ in range(3):
            tokens = line()
            if tokens[0] != 'vertex':
                raise InvalidAsset('Expected vertex.')
            vertices.append(numbers(tokens[1:]))
        if line() != ['endloop'] or line() != ['endfacet']:
            raise InvalidAsset('Expected endloop and endfacet.')
        yield vertices


def binary_triangles(data, count):
    for index in range(count):
        values = struct.unpack_from('<12fH', data, 84 + index * 50)
        if not all(math.isfinite(value) for value in values[:12]):
            raise InvalidAsset('Nonfinite coordinate or normal.')
        yield [values[3:6], values[6:9], values[9:12]]


def inspect_stl(data):
    count = struct.unpack_from('<I', data, 80)[0] if len(data) >= 84 else None
    if count is not None and len(data) == 84 + count * 50:
        encoding, triangles = 'binary', binary_triangles(data, count)
    else:
        encoding, triangles = 'ascii', ascii_triangles(data)
    low, high = [math.inf] * 3, [-math.inf] * 3
    total = degenerate = 0
    for vertices in triangles:
        total += 1
        for vertex in vertices:
            for axis in range(3):
                low[axis] = min(low[axis], vertex[axis])
                high[axis] = max(high[axis], vertex[axis])
        scale = max(abs(value) for vertex in vertices for value in vertex)
        if scale == 0:
            degenerate += 1
        else:
            a, b, c = [[value / scale for value in vertex] for vertex in vertices]
            u, v = [b[i] - a[i] for i in range(3)], [c[i] - a[i] for i in range(3)]
            cross = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
            degenerate += int(all(value == 0 for value in cross))
    if total == 0:
        raise InvalidAsset('STL contains no triangles.')
    extent = [high[i] - low[i] for i in range(3)]
    if not all(math.isfinite(value) for value in extent):
        raise InvalidAsset('Extent exceeds representable numeric range.')
    return {'status': 'inspected', 'encoding': encoding, 'triangle_count': total,
            'numeric_zero_area_triangles': degenerate,
            'bounds': {'min': low, 'max': high, 'extent': extent},
            'warnings': ['Numeric zero-area triangles found.'] if degenerate else []}


def inspect(path, units=None, max_bytes=MAX_BYTES):
    result = {'schema_version': 1, 'path': str(Path(path).absolute()), 'status': 'error',
              'units': units or 'unknown', 'units_source': 'user_asserted' if units else 'unknown',
              'fingerprint': {'status': 'not_checked'}, 'geometry': {'status': 'not_checked'},
              'limitations': LIMITATIONS}
    if Path(path).suffix.lower() not in ('.stl', '.3mf'):
        result.update(units='unknown', units_source='not_inspected', limitations=[
            'File bytes and identity only; the format and embedded units have not been parsed.',
            'No geometry, topology, dimensions, settings, or manufacturability checks.',
            'Inspection describes captured bytes, not a future version or a machine job.'])
    if Path(path).suffix.lower() == '.3mf':
        result.update(schema_version=2, units='unknown', units_source='not_verified', limitations=[
            'Partial 3MF inspection only; no XSD/OPC conformance, topology, world bounds, settings, or manufacturing approval.',
            'Failed inspection establishes no model units or geometry; a fingerprint alone is not validation.'])
    try:
        # Nonblocking open prevents hanging on FIFOs. fstat checks the opened target.
        fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_BINARY', 0))
        with os.fdopen(fd, 'rb') as source:
            before = os.fstat(source.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise InvalidAsset('Input must be a regular file.')
            if before.st_size > max_bytes:
                raise InvalidAsset('File exceeds the configured byte limit; fingerprint not computed.')
            data = source.read(max_bytes + 1)
            after = os.fstat(source.fileno())
        if len(data) > max_bytes:
            raise InvalidAsset('Input grew beyond the configured byte limit.')
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise InvalidAsset('Input changed during inspection; retry against a frozen copy.')
        result['fingerprint'] = {'status': 'inspected', 'sha256': hashlib.sha256(data).hexdigest(), 'byte_size': len(data)}
        if not data:
            raise InvalidAsset('Input is empty.')
        if units is not None and Path(path).suffix.lower() != '.stl':
            raise InvalidAsset('--units applies only to STL; other formats require their own unit inspection.')
        if Path(path).suffix.lower() == '.3mf':
            result['geometry'] = inspect_3mf(data)
            result.update(status='partial', schema_version=2, units=result['geometry']['units'],
                          units_source=result['geometry']['units_source'],
                          limitations=result['geometry']['gaps'])
            return result, 3
        if Path(path).suffix.lower() != '.stl':
            result.update(status='metadata_only', geometry={'status': 'unsupported', 'reason': 'Only STL and partial 3MF inspection are implemented; extension does not validate format.'})
            return result, 3
        result['geometry'] = inspect_stl(data)
        result['status'] = 'inspected'
        return result, 0
    except (OSError, InvalidAsset, Invalid3MF) as exc:
        result['error'] = str(exc)
        result['geometry']['status'] = 'not_verified'
        return result, 2


def byte_limit(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Byte limit must be an integer.') from exc
    if not 1 <= number <= MAX_BYTES:
        raise argparse.ArgumentTypeError('Byte limit must be 1 through 67108864.')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path')
    parser.add_argument('--units', choices=['mm', 'cm', 'm', 'in'], help='User-asserted STL units; no conversion.')
    parser.add_argument('--max-bytes', type=byte_limit, default=MAX_BYTES, help='Lower the 64 MiB read limit.')
    args = parser.parse_args()
    result, code = inspect(args.path, args.units, args.max_bytes)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return code


if __name__ == '__main__':
    sys.exit(main())

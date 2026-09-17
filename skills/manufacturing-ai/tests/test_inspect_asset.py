"""Observable CLI tests. Run: python3 -m unittest discover -s tests -v"""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'inspect_asset.py'
ASCII = b'''solid demo
facet normal 0 0 1
outer loop
vertex -1 0 0
vertex 2 0 0
vertex 0 4 0
endloop
endfacet
endsolid demo
'''


def binary(header=b'binary', vertices=(-1, 0, 0, 2, 0, 0, 0, 4, 0)):
    return header.ljust(80, b' ') + struct.pack('<I12fH', 1, 0, 0, 1, *vertices, 0)


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_asset(self, data, suffix='.stl', extra=()):
        path = self.root / ('asset' + suffix)
        path.write_bytes(data)
        before = path.stat()
        process = subprocess.run([sys.executable, str(SCRIPT), str(path), *extra], capture_output=True, text=True, timeout=10)
        self.assertEqual(path.read_bytes(), data)
        self.assertEqual(path.stat().st_mtime_ns, before.st_mtime_ns)
        self.assertEqual(process.stderr, '')
        return process.returncode, json.loads(process.stdout), process.stdout

    def test_ascii_bounds_fingerprint_unknown_units_and_repeatability(self):
        code, report, output = self.run_asset(ASCII)
        self.assertEqual(code, 0)
        self.assertEqual(report['fingerprint']['sha256'], hashlib.sha256(ASCII).hexdigest())
        self.assertEqual(report['fingerprint']['byte_size'], len(ASCII))
        self.assertEqual(report['units'], 'unknown')
        self.assertEqual(report['geometry']['bounds'], {'min': [-1, 0, 0], 'max': [2, 4, 0], 'extent': [3, 4, 0]})
        self.assertEqual(report['geometry']['triangle_count'], 1)
        self.assertEqual(report['geometry']['numeric_zero_area_triangles'], 0)
        self.assertEqual(self.run_asset(ASCII)[2], output)

    def test_binary_header_may_start_solid_and_units_do_not_scale(self):
        code, report, _ = self.run_asset(binary(b'solid misleading'), extra=['--units', 'in'])
        self.assertEqual(code, 0)
        self.assertEqual(report['geometry']['encoding'], 'binary')
        self.assertEqual(report['geometry']['bounds']['extent'], [3, 4, 0])
        self.assertEqual(report['units_source'], 'user_asserted')

    def test_multifacet_translated_geometry_checks_every_triangle(self):
        # Four faces of a translated tetrahedron, including bounds absent from face 1.
        a, b, c, d = (5, -2, 1), (8, -2, 1), (5, 2, 1), (5, -2, 6)
        faces = [(a, b, c), (a, d, b), (a, c, d), (b, d, c)]
        payload = b'tetra'.ljust(80, b' ') + struct.pack('<I', len(faces))
        for face in faces:
            payload += struct.pack('<12fH', 0, 0, 0, *(v for vertex in face for v in vertex), 0)
        code, report, _ = self.run_asset(payload)
        self.assertEqual(code, 0)
        self.assertEqual(report['geometry']['triangle_count'], 4)
        self.assertEqual(report['geometry']['bounds'],
                         {'min': [5, -2, 1], 'max': [8, 2, 6], 'extent': [3, 4, 5]})
        self.assertEqual(report['geometry']['numeric_zero_area_triangles'], 0)

    def test_zero_area_reported_without_approval(self):
        code, report, _ = self.run_asset(binary(vertices=(0, 0, 0, 1, 0, 0, 2, 0, 0)))
        self.assertEqual(code, 0)
        self.assertEqual(report['geometry']['numeric_zero_area_triangles'], 1)
        self.assertTrue(report['geometry']['warnings'])
        self.assertNotIn('approved', report)

    def test_malformed_geometry_is_rejected_without_partial_bounds(self):
        for data in [b'', b'solid empty\nendsolid empty', binary()[:-1], binary()+b'junk',
                     ASCII.replace(b'endloop', b'oops'), ASCII.replace(b'2 0 0', b'nan 0 0'),
                     ASCII.replace(b'2 0 0', b'inf 0 0'), ASCII.replace(b'endfacet', b''),
                     ASCII + b'solid another\nendsolid another', binary(vertices=(float('nan'),)*9),
                     ASCII.replace(b'-1 0 0', b'-1e308 0 0').replace(b'2 0 0', b'1e308 0 0')]:
            with self.subTest(data=data):
                code, report, _ = self.run_asset(data)
                self.assertEqual(code, 2)
                self.assertEqual(report['geometry']['status'], 'not_verified')
                self.assertNotIn('bounds', report['geometry'])

    def test_other_formats_get_only_fingerprint(self):
        for suffix in ['.step', '.obj', '.svg', '.glb', '.txt']:
            with self.subTest(suffix=suffix):
                code, report, _ = self.run_asset(b'not necessarily valid format', suffix=suffix)
                self.assertEqual(code, 3)
                self.assertEqual(report['status'], 'metadata_only')
                self.assertEqual(report['geometry']['status'], 'unsupported')
                self.assertEqual(report['fingerprint']['status'], 'inspected')

    def test_metadata_only_does_not_infer_units_or_reuse_stl_claims(self):
        code, report, _ = self.run_asset(b'opaque format contents', suffix='.step')
        self.assertEqual(code, 3)
        self.assertEqual(report['units'], 'unknown')
        self.assertEqual(report['units_source'], 'not_inspected')
        self.assertTrue(all('STL' not in item for item in report['limitations']))
        self.assertEqual(report['geometry']['status'], 'unsupported')

    def test_stl_unit_flag_rejected_for_unparsed_formats(self):
        for suffix in ['.step', '.svg', '.obj', '.txt']:
            with self.subTest(suffix=suffix):
                code, report, _ = self.run_asset(b'opaque', suffix=suffix, extra=['--units', 'mm'])
                self.assertEqual(code, 2)
                self.assertEqual(report['units'], 'unknown')
                self.assertEqual(report['geometry']['status'], 'not_verified')
                self.assertEqual(report['fingerprint']['status'], 'inspected')

    def test_oversized_ascii_line_is_rejected(self):
        for data in [b'solid ' + b'x' * 4096 + b'\n' + ASCII.split(b'\n', 1)[1],
                     ASCII.replace(b'vertex -1 0 0', b'vertex ' + b'1' * 5000 + b' 0 0')]:
            with self.subTest(size=len(data)):
                code, report, _ = self.run_asset(data)
                self.assertEqual(code, 2)
                self.assertIn('4096-byte limit', report['error'])
                self.assertEqual(report['geometry']['status'], 'not_verified')
                self.assertEqual(report['fingerprint']['status'], 'inspected')

    def test_invalid_cli_options_fail_with_argument_error(self):
        path = self.root / 'valid.stl'
        path.write_bytes(ASCII)
        for options in [['--max-bytes', '0'], ['--max-bytes', '-1'],
                        ['--max-bytes', '67108865'], ['--max-bytes', 'lots'],
                        ['--units', 'feet']]:
            with self.subTest(options=options):
                process = subprocess.run([sys.executable, str(SCRIPT), str(path), *options],
                                         capture_output=True, text=True, timeout=10)
                self.assertEqual(process.returncode, 2)
                self.assertEqual(process.stdout, '')
                self.assertIn('error:', process.stderr)
                self.assertEqual(path.read_bytes(), ASCII)

    def test_byte_limit_stops_before_fingerprint(self):
        code, report, _ = self.run_asset(ASCII, extra=['--max-bytes', '10'])
        self.assertEqual(code, 2)
        self.assertEqual(report['fingerprint']['status'], 'not_checked')

    def test_missing_and_directory_inputs_return_json_errors(self):
        for path in [self.root / 'missing.stl', self.root]:
            process = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, timeout=10)
            self.assertEqual(process.returncode, 2)
            self.assertEqual(json.loads(process.stdout)['status'], 'error')

    @unittest.skipUnless(hasattr(__import__('os'), 'mkfifo'), 'Requires FIFO support')
    def test_fifo_does_not_block(self):
        import os
        path = self.root / 'pipe.stl'
        os.mkfifo(path)
        process = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, timeout=3)
        self.assertEqual(process.returncode, 2)
        self.assertIn('regular file', json.loads(process.stdout)['error'])


if __name__ == '__main__':
    unittest.main()

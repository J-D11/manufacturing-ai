import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_print_job import inspect

class PrintJobTest(unittest.TestCase):
    def job(self, text, checksum=None):
        tmp = tempfile.NamedTemporaryFile(suffix='.3mf', delete=False)
        tmp.close()
        self.addCleanup(Path(tmp.name).unlink)
        with zipfile.ZipFile(tmp.name, 'w') as z:
            z.writestr('Metadata/plate_1.gcode', text)
            z.writestr('Metadata/plate_1.gcode.md5', checksum or hashlib.md5(text.encode()).hexdigest())
            z.writestr('Metadata/project_settings.config', json.dumps({'printer_model':'P1S','nozzle_diameter':['0.4']}))
        return tmp.name
    def test_comment_not_pause(self):
        self.assertTrue(inspect(self.job('; machine_pause_gcode = M400 U1\n'))['passed'])
    def test_actual_pause_and_wrong_layer(self):
        p=self.job('; layer num/total_layer_count: 25/30\nM400 U1\n')
        self.assertTrue(inspect(p,[25],'P1S',.4)['passed'])
        self.assertFalse(inspect(p,[24])['passed'])
    def test_corrupt_checksum(self):
        self.assertFalse(inspect(self.job('G1 X1','bad'))['passed'])
    def test_wrong_profile(self):
        self.assertFalse(inspect(self.job('G1 X1'),printer='A1',nozzle=.2)['passed'])
    def test_inherited_pause(self):
        self.assertFalse(inspect(self.job('M400 U1'))['passed'])
    def test_other_pause(self):
        self.assertFalse(inspect(self.job('M25'))['passed'])
if __name__=='__main__':unittest.main()

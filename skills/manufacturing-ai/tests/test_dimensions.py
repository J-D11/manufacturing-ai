import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_dimensions import check
class DimensionsTest(unittest.TestCase):
    def test_dependent_feature_drift(self):
        d={'measurements':{'base':3,'offset':1.2,'recess':4.2},'checks':[{'name':'recess follows base','left':['base','offset'],'right':['recess'],'relation':'eq'}]}
        self.assertTrue(check(d)['passed'])
        d['measurements']['recess']=4.6
        self.assertFalse(check(d)['passed'])
    def test_nonfinite(self):
        with self.assertRaises(ValueError):check({'measurements':{'x':float('nan')},'checks':[]})
    def test_empty(self):
        with self.assertRaises(ValueError):check({'measurements':{},'checks':[]})

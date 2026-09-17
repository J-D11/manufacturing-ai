"""Check CAD-exported dimensional relationships from JSON; never evaluates code.
Input: {measurements: {name: mm}, checks: [{name, left: [names], right: [names],
relation: eq|ge|le, tolerance: mm}]}. Extract measurements from current CAD or mesh,
not duplicated design intent. Hash the measured artifact in the project record.
"""
import argparse
import json
import math

def check(document):
    m = document['measurements']
    if not all(isinstance(v, (float, int)) and not isinstance(v, bool) and math.isfinite(v) for v in m.values()):
        raise ValueError('Measurements must be finite numbers in mm')
    results = []
    for c in document['checks']:
        left = sum(m[k] for k in c['left'])
        right = sum(m[k] for k in c['right'])
        t = c.get('tolerance', .001)
        if not isinstance(t, (float, int)) or not math.isfinite(t) or t < 0:
            raise ValueError('Invalid tolerance')
        r = c['relation']
        if r not in ('eq', 'ge', 'le'):
            raise ValueError('Unknown relationship')
        passed = abs(left-right) <= t if r == 'eq' else left >= right-t if r == 'ge' else left <= right+t
        results.append({'name': c['name'], 'passed': passed, 'left_mm': left, 'right_mm': right})
    if not results:
        raise ValueError('No dimensional checks provided')
    return {'passed': all(c['passed'] for c in results), 'checks': results,
            'limits': 'Verifies supplied measurements only; does not extract geometry or prove physical fit.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__);p.add_argument('measurements');a=p.parse_args()
    try:
        with open(a.measurements) as f: result=check(json.load(f))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        result={'passed':False,'error':str(exc)}
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)

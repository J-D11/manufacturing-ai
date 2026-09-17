"""Read-only native Bambu job identity/profile/pause check, not print certification."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile


def inspect(path, pauses=(), printer=None, nozzle=None):
    path = Path(path)
    if path.stat().st_size > 128 * 1024 * 1024:
        raise ValueError('Package exceeds 128 MiB limit')
    errors = []
    with zipfile.ZipFile(path) as z:
        entries = z.infolist()
        names = [i.filename for i in entries]
        if len(names) != len(set(names)) or len(entries) > 256:
            raise ValueError('Duplicate ZIP names or excessive entries')
        if sum(i.file_size for i in entries) > 256 * 1024 * 1024:
            raise ValueError('Expanded package exceeds 256 MiB limit')
        if any(i.file_size > 128 * 1024 * 1024 or i.flag_bits & 1 for i in entries):
            raise ValueError('Oversized or encrypted member')
        if z.testzip() is not None:
            raise ValueError('ZIP CRC failure')
        jobs = [n for n in names if re.fullmatch(r'Metadata/plate_\d+\.gcode', n)]
        if len(jobs) != 1:
            raise ValueError('Requires exactly one sliced plate; audit other layouts separately')
        data = z.read(jobs[0])
        expected_md5 = z.read(jobs[0] + '.md5').decode().strip().lower()
        if hashlib.md5(data).hexdigest() != expected_md5:
            errors.append('G-code MD5 mismatch')
        cfg = json.loads(z.read('Metadata/project_settings.config'))
        if printer and cfg.get('printer_model') != printer:
            errors.append('Printer model mismatch')
        diameters = cfg.get('nozzle_diameter', [])
        if nozzle is not None and (not diameters or any(abs(float(v)-nozzle) > 1e-6 for v in diameters)):
            errors.append('Nozzle diameter mismatch')
        layers, found, unsupported = None, [], []
        for line in data.decode('utf-8').splitlines():
            match = re.match(r'; layer num/total_layer_count:\s*(\d+)/', line)
            if match:
                layers = int(match.group(1))
            command = line.split(';', 1)[0].strip()
            if re.fullmatch(r'M400\s+U1', command):
                found.append(layers)
            elif re.match(r'^(?:M0|M1|M25|M600)(?:\s|$)', command):
                unsupported.append(command)
        if found != list(pauses):
            errors.append('Insertion pause layers differ from expectation')
        if unsupported:
            errors.append('Other pause/change commands require manual review')
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'printer': cfg.get('printer_model'), 'nozzle': diameters,
            'colors': cfg.get('filament_colour'), 'pause_layers': found,
            'errors': errors, 'passed': not errors,
            'limits': 'No geometry, collision, sealing-layer, AMS, or physical readiness verification.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('job')
    p.add_argument('--pauses', nargs='*', type=int, default=[])
    p.add_argument('--printer')
    p.add_argument('--nozzle', type=float)
    a = p.parse_args()
    try:
        result = inspect(a.job, a.pauses, a.printer, a.nozzle)
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, RuntimeError) as exc:
        result = {'passed': False, 'errors': [str(exc)]}
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

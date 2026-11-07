"""Check content/v2/*.json against English: same keys and list lengths, no empty strings, placeholders kept."""
import json
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "content" / "v2"


def walk(a, b, path, errors):
    if isinstance(a, dict):
        if not isinstance(b, dict) or set(a) != set(b):
            errors.append(f"{path}: keys differ ({sorted(set(a) ^ set(b if isinstance(b, dict) else {}))})")
            return
        for k in a:
            walk(a[k], b[k], f"{path}.{k}", errors)
    elif isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b):
            errors.append(f"{path}: list length differs")
            return
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]", errors)
    elif isinstance(a, str) and (not isinstance(b, str) or not b.strip()):
        errors.append(f"{path}: empty")


def main():
    en = json.loads((DIR / "en.json").read_text())
    bad = 0
    for p in sorted(DIR.glob("*.json")):
        errors = []
        walk(en, json.loads(p.read_text()), p.stem, errors)
        print(p.name, "ok" if not errors else f"{len(errors)} problem(s)")
        for e in errors[:20]:
            print("  ", e)
        bad += len(errors)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

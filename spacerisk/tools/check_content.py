"""Check that every content/<lang>.json has exactly the structure of content/en.json (keys, list lengths, fixed fields)."""
import json
import sys
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "content"
FIXED = {"file", "icon", "image"}  # must stay identical to English


def compare(en, other, path, problems):
    if isinstance(en, dict):
        if not isinstance(other, dict):
            return problems.append(f"{path}: expected object")
        if path == "$.sectors.groups":  # group names are translated keys: compare values in order
            if len(en) != len(other):
                problems.append(f"{path}: {len(other)} groups, expected {len(en)}")
            for (ek, ev), (ok, ov) in zip(en.items(), other.items()):
                compare(ev, ov, f"{path}[{ek}]", problems)
            return
        if set(en) != set(other):
            problems.append(f"{path}: keys differ: missing {sorted(set(en) - set(other))}, extra {sorted(set(other) - set(en))}")
        for k in en:
            if k in other:
                if k in FIXED and en[k] != other[k]:
                    problems.append(f"{path}.{k}: must stay '{en[k]}'")
                compare(en[k], other[k], f"{path}.{k}", problems)
    elif isinstance(en, list):
        if not isinstance(other, list) or len(en) != len(other):
            return problems.append(f"{path}: list length {len(other) if isinstance(other, list) else '?'} != {len(en)}")
        for i, (a, b) in enumerate(zip(en, other)):
            compare(a, b, f"{path}[{i}]", problems)
    elif isinstance(en, str) and (not isinstance(other, str) or not other.strip()):
        problems.append(f"{path}: expected non-empty text")


if __name__ == "__main__":
    en = json.loads((CONTENT / "en.json").read_text())
    bad = 0
    for p in sorted(CONTENT.glob("*.json")):
        if p.stem == "en":
            continue
        problems = []
        compare(en, json.loads(p.read_text()), "$", problems)
        print(f"{p.name}: {'OK' if not problems else str(len(problems)) + ' problems'}")
        for x in problems[:30]:
            print("  -", x)
        bad += bool(problems)
    sys.exit(1 if bad else 0)

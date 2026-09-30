from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
DOCS = ROOT / "docs"


REQUIRED = [
    EVIDENCE / "PUBLIC_EVIDENCE_MANIFEST.json",
    EVIDENCE / "README_PUBLIC_EVIDENCE.md",
    EVIDENCE / "SHA256SUMS.txt",
    EVIDENCE / "Suchergebnisse_admon395_PAGE1_PUBLIC_SAFE.html",
    DOCS / "admon395_lesefassung_16_jahre_spaeter.md",
    DOCS / "admon395_wesens_realitaet_lucinet_lesebuch_band1.pdf",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.exists()]
    if missing:
        print(json.dumps({"ok": False, "missing": missing}, indent=2))
        return 1

    manifest = json.loads((EVIDENCE / "PUBLIC_EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))
    expected_html = manifest["raw_source_sha256"]
    public_html_hash = sha256(EVIDENCE / "Suchergebnisse_admon395_PAGE1_PUBLIC_SAFE.html")

    sums = (EVIDENCE / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    declared = {}
    for line in sums:
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        declared[name.strip()] = digest.strip().lower()

    checked = {}
    for name, digest in declared.items():
        path = EVIDENCE / name
        if not path.exists():
            print(json.dumps({"ok": False, "missing_declared_file": name}, indent=2))
            return 1
        actual = sha256(path)
        checked[name] = actual
        if actual.lower() != digest:
            print(json.dumps({"ok": False, "hash_mismatch": name, "expected": digest, "actual": actual}, indent=2))
            return 1

    result = {
        "ok": True,
        "account": manifest.get("account_name"),
        "account_user_id": manifest.get("account_user_id"),
        "search_result_total": manifest.get("search_result_total"),
        "search_result_pages": manifest.get("search_result_pages"),
        "public_html_sha256": public_html_hash,
        "raw_source_sha256_from_manifest": expected_html,
        "checked_files": checked,
        "claim_ceiling": "public-safe derivative verified; raw source hash referenced, not rederived",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


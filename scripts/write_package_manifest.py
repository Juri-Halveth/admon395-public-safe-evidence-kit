from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "PACKAGE_MANIFEST.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


files = []
for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(".git/") or rel == "analysis.page1.json" or rel == "PACKAGE_MANIFEST.json":
        continue
    files.append(
        {
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
    )

manifest = {
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "package": "admon395_github_materialization_kit",
    "publication_state": "LOCAL_PREPARED_NOT_PUSHED",
    "file_count": len(files),
    "files": files,
}

OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUT)

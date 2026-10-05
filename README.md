<!-- HUB_LANGUAGES_V1 -->
[Original / Deutsch](README.md) · [English](README.en.md) · [Русский](README.ru.md)
<!-- /HUB_LANGUAGES_V1 -->

# ADMON395 Public-Safe Evidence Kit

This repository preserves and analyzes a public-safe evidence package for the
account-bound forum search page `admon395`.

It is designed as a reproducible reading and evidence kit: source bytes, hashes,
scripts, generated reading material, and a proof matrix are kept together.

## What Is Here

- `evidence/` contains the public-safe source material:
  - `PUBLIC_EVIDENCE_MANIFEST.json`
  - `README_PUBLIC_EVIDENCE.md`
  - `SHA256SUMS.txt`
  - `Suchergebnisse_admon395_PAGE1_PUBLIC_SAFE.html`
- `docs/` contains generated reader-facing outputs:
  - `ADMON395_PROOF_MATRIX_2026-10-01.md`
  - `admon395_lesefassung_16_jahre_spaeter.md`
  - `admon395_wesens_realitaet_lucinet_lesebuch_band1.pdf`
- `scripts/` contains the local analysis and PDF builder scripts.
- `.github/workflows/verify.yml` defines a basic reproducibility check.

## Evidence Boundary

The material supports this bounded statement:

> A public-safe derivative of a saved forum search page attributes visible
> search results to account `admon395` / user ID `25721`, with the raw source
> bound by SHA-256 in the manifest.

It does not by itself prove:

- physical authorship behind every keyboard event;
- truth of the described experiences;
- external causation;
- medical, metaphysical, legal, or security conclusions;
- complete coverage of all forum posts.

The manifest says the full search had 71 results on 3 pages. This kit currently
contains only page 1, with 25 visible results.

## Reproduce

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

Run checks:

```powershell
py scripts\verify_package.py
```

Extract the structured page-one result summary:

```powershell
py scripts\analyze_admon_html.py
```

The PDF in `docs/` is included as a generated artifact. It can be regenerated
from the included public-safe source page:

```powershell
py scripts\build_admon395_pdf.py
```

## Publication Status

Observed materialization state on 2026-10-01:

```text
LOCAL_PREPARED: yes
GITHUB_REPOSITORY: https://github.com/Juri-Halveth/admon395-public-safe-evidence-kit
GITHUB_VISIBILITY: public
DEFAULT_BRANCH: master
REMOTE_HEAD: 4f1e16a4fc727d872d91fa346d2429e13f474980 before proof-matrix update
CI_ACCEPTED: yes, run 36794087311
RELEASE: v0.1.0-public-safe
```

Future pushes, release updates, or public announcements remain separate
materialization steps and should be recorded with their own receipt.

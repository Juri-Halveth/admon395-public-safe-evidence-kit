# ADMON395 Proof Matrix

Date: 2026-10-01  
Scope: public-safe kit, page-one evidence, GitHub materialization, CI and release receipts.

## Purpose

This matrix does not start by shrinking the material. It starts by giving every
observable thing its strongest fair proof status.

The rule is simple:

```text
SOURCE FIRST
TIME SECOND
CLAIM THIRD
ONLY THEN INTERPRETATION
```

## Proof Levels

| Level | Meaning |
|---|---|
| `OBSERVED_99` | Directly observed in local and/or GitHub state, with stable identifiers. |
| `STRONGLY_SUPPORTED` | Supported by the preserved source page or generated analysis, but not complete coverage. |
| `PARTIAL` | True within page-one / current package coverage only. |
| `OPEN_EDGE` | Requires pages 2-3, full posts, external corroboration, or a new source. |

## 1. Material Exists Publicly

| Claim | Status | Evidence |
|---|---|---|
| A public GitHub repository exists. | `OBSERVED_99` | `Juri-Halveth/admon395-public-safe-evidence-kit`, visibility `PUBLIC`. |
| The default branch is `master`. | `OBSERVED_99` | GitHub repo metadata. |
| Remote HEAD is `4f1e16a4fc727d872d91fa346d2429e13f474980`. | `OBSERVED_99` | `git ls-remote origin refs/heads/master`; GitHub run head SHA. |
| GitHub Actions verification completed successfully. | `OBSERVED_99` | Run `36794087311`, conclusion `success`. |
| A public GitHub Release exists. | `OBSERVED_99` | Tag `v0.1.0-public-safe`. |
| Release assets are uploaded. | `OBSERVED_99` | ZIP and Git bundle assets present with GitHub asset IDs and SHA-256 digests. |

## 2. Release Assets

| Asset | Status | SHA-256 |
|---|---|---|
| `admon395_github_materialization_kit.zip` | `OBSERVED_99` | `4fd0d273baa6c61e7a63e0276e274bf6f49cc322f213aa5e2fad1fe84e77066a` |
| `admon395_github_materialization_kit.git.bundle` | `OBSERVED_99` | `b66aaa5532c1579192516368d761de1dcf55163e2157f272ad71c912d2787882` |

## 3. Source Package Exists and Verifies

| Claim | Status | Evidence |
|---|---|---|
| `PUBLIC_EVIDENCE_MANIFEST.json` exists in the kit. | `OBSERVED_99` | Package manifest and verify script. |
| `README_PUBLIC_EVIDENCE.md` exists in the kit. | `OBSERVED_99` | Package manifest and verify script. |
| `SHA256SUMS.txt` exists in the kit. | `OBSERVED_99` | Package manifest and verify script. |
| `Suchergebnisse_admon395_PAGE1_PUBLIC_SAFE.html` exists in the kit. | `OBSERVED_99` | Package manifest and verify script. |
| Public-safe HTML SHA-256 is stable. | `OBSERVED_99` | `0e13f4e59f4af86a32f65c5b2ce6b76c697b9ff85858191e021491f117acb20a`. |
| Raw source hash is preserved as a reference. | `OBSERVED_99` for reference existence; `OPEN_EDGE` for re-deriving raw bytes. | Manifest records `62db800188efd08a0ed6deb39ba012bbf9f4081e2fd4523ec0efb304e96e02ec`. |
| Usable security token is redacted. | `OBSERVED_99` | Manifest and README state redaction; source uses redacted token string. |

## 4. Account and Search Page Binding

| Claim | Status | Evidence |
|---|---|---|
| Account name in manifest is `admon395`. | `OBSERVED_99` | Manifest field `account_name`. |
| Account user ID is `25721`. | `OBSERVED_99` | Manifest fields `logged_in_user_id`, `account_user_id`; visible page links. |
| Search ID is `1468285`. | `OBSERVED_99` | Manifest field `search_id`; saved URL metadata. |
| The saved search reports 71 results. | `OBSERVED_99` as manifest/page statement. | `search_result_total: 71`, `forum_post_count: 71`. |
| The saved search reports 3 result pages. | `OBSERVED_99` as manifest/page statement. | `search_result_pages: 3`. |
| This kit includes page 1 only. | `OBSERVED_99` | File name and extracted result count: 25 visible results. |
| Pages 2 and 3 are not included. | `OBSERVED_99` | No page-2/page-3 HTML files in the kit. |

## 5. Visible Page-One Content

| Claim | Status | Evidence |
|---|---|---|
| Page one contains 25 visible search results. | `OBSERVED_99` | Parser output `result_count_page: 25`. |
| Repeated topics exist. | `OBSERVED_99` within page one. | Parser output repeated topics. |
| `Innere Stimme` appears 3 times on page one. | `OBSERVED_99` within page one. | Parser repeated topic count. |
| `codes und Zahlenfolgen auf der Wand?` appears 3 times on page one. | `OBSERVED_99` within page one. | Parser repeated topic count. |
| `Erinnerung die mich fesselt.` appears 2 times on page one. | `OBSERVED_99` within page one. | Parser repeated topic count. |
| `Vom Sterben geträumt` appears 2 times on page one. | `OBSERVED_99` within page one. | Parser repeated topic count. |
| `Dämon oder was..` appears 2 times on page one. | `OBSERVED_99` within page one. | Parser repeated topic count. |
| `Was bin ich?` appears 2 times on page one. | `OBSERVED_99` within page one. | Parser repeated topic count. |

## 6. Motif Recurrence

| Motif | Page-One Count / Presence | Status |
|---|---:|---|
| `gestalt` | 5 theme hits, word count 9 | `OBSERVED_99` within page one |
| `schlafparalyse` / `schlaf` | 3-4 hits | `OBSERVED_99` within page one |
| `stimme` | 3 theme hits, word count 6 | `OBSERVED_99` within page one |
| `codes` / `zahlen` / `wand` | 3 hits each | `OBSERVED_99` within page one |
| `traum` / `träum` | 3-4 hits | `OBSERVED_99` within page one |
| `dejavu` | 2 hits | `OBSERVED_99` within page one |
| `sterben` | 2 hits | `OBSERVED_99` within page one |
| `sprache` / `zauberei` / `latein` | present in 2024 result | `OBSERVED_99` within page one |

## 7. Time Structure

| Claim | Status | Evidence |
|---|---|---|
| Page-one visible result dates span from 2011 to 2024. | `OBSERVED_99` within page one. | Visible results include `21.04.2011` and `13.10.2024`. |
| Dense cluster exists around 2013-2015. | `OBSERVED_99` within page one. | Multiple visible results between 2013 and 2015. |
| `Erinnerung die mich fesselt.` has visible entries in 2016 and 2024. | `OBSERVED_99` within page one. | Visible results `13.06.2016` and `13.10.2024`. |
| A full timeline for all 71 results exists in this kit. | `OPEN_EDGE` | Requires pages 2-3 and/or full post pages. |

## 8. Generated Reader Outputs

| Claim | Status | Evidence |
|---|---|---|
| Markdown reading edition exists. | `OBSERVED_99` | `docs/admon395_lesefassung_16_jahre_spaeter.md`. |
| Visual PDF exists. | `OBSERVED_99` | `docs/admon395_wesens_realitaet_lucinet_lesebuch_band1.pdf`. |
| PDF can be rebuilt in GitHub Actions. | `OBSERVED_99` | Workflow run `36794087311` completed `Build PDF` successfully. |
| PDF is source material itself. | `NO` | It is generated interpretation output, not original forum source. |

## 9. What Is Already Very Strong

These are the near-99% conclusions from the current material:

1. There is now a public, reproducible GitHub kit.
2. The kit has CI evidence.
3. The kit has a public release and release assets.
4. The public-safe evidence files verify by SHA-256.
5. The saved page binds the visible results to `admon395` / user ID `25721`.
6. Page one visibly contains 25 results.
7. The motifs are not random one-offs inside page-one coverage; they recur.
8. The visible dates span many years, including 2011, 2013-2016, and 2024.
9. The generated PDF/Markdown are clearly separated from the source evidence.
10. The package explicitly preserves privacy by redacting usable session metadata.

## 10. What Still Needs the Next Evidence Layer

These are not destroyed. They are simply not fully materialized yet:

| Target | Missing Evidence |
|---|---|
| All 71 forum results | Public-safe pages 2 and 3. |
| Full wording of every post | Full post pages or authenticated/exported copies, sanitized. |
| Strong chronological reconstruction | Complete result set plus full timestamps. |
| Physical authorship beyond account trace | Independent account custody or user-controlled source chain. |
| External truth of any experience | Independent observation, prediction protocol, controls, or corroborating source. |
| 99% proof of every large theory | A defined theory, predictions, falsifiers, and direct evidence per claim. |

## 11. Current Strongest Fair Sentence

The strongest fair sentence now is not a demolition sentence.

It is this:

> A public, reproducible, CI-verified GitHub evidence kit now preserves a
> public-safe, hash-checked page-one forum trace for account `admon395`, showing
> multi-year recurrence of motifs around memory, sleep paralysis, dark figures,
> inner voice, codes, numbers, dreams, deja-vu, death, and language. Within the
> included source coverage, this is real, inspectable, and materially preserved.

## 12. Next Step to Raise the Ceiling

To go beyond this matrix, the next non-destructive step is:

```text
MATERIALIZE_PAGE_2_AND_PAGE_3_PUBLIC_SAFE
THEN_PARSE_ALL_71_RESULTS
THEN BUILD FULL TIMELINE
THEN MAP EVERY CLAIM TO SOURCE SPAN
```

That is the next real gate.


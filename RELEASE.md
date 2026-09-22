# Proposed release and rights provenance

This is a local review packet. No file is authorized for external release by this folder alone.

## Exact proposed release list

If a later release decision names this packet, the proposed file list is exactly:

- `README.md`
- `TASKS.md`
- `SUBMIT.md`
- `FLOW.md`
- `task.schema.json`
- `task.json`
- `ai-task.json`
- `report.schema.json`
- `report.template.json`
- `examples/water-case.json`
- `check_packet.py`
- `tests/test_check_packet.py`

`OUTREACH_UNSENT.md` is an internal draft and is excluded from the proposed public packet. `RELEASE.md` is a review/provenance record and is included only if the release decision explicitly includes it.

The validator and its test file are included in this proposal so the README's local check is reproducible. `RESULTS.md` remains an internal validation record, excluded unless a later release record explicitly adds it.

## Provenance and rights

- `README.md`, `TASKS.md`, `SUBMIT.md`, `FLOW.md`, the JSON schemas, `task.json`, `report.template.json`, `examples/water-case.json`, and this record are original text and structure prepared for this packet by the Governance Lab workstream. The fictional water case is original and contains no private archive material.
- `ai-task.json` and `check_packet.py` are original code/data prepared for this packet. `report.template.json` is an original worked example intended to be edited; it is not a contributor submission or evidence of actual work.
- `tests/` and `RESULTS.md` are original validation code and reporting prepared for this packet; only the specifically listed test file is proposed for external release.
- The packet paraphrases themes from *The Good Work* and points readers to project source-grounding records; it includes no verbatim source excerpt. The supplied source file is not copied into this packet.
- No third-party source code is copied into this packet. The proposed validator uses Python's standard library; no Python runtime is bundled. Redistribution terms for all artifacts still need an explicit release record.
- The inspected project records do not state a license or reuse authorization for the supplied *The Good Work* text or for all surrounding project materials. This packet therefore grants no license, permission, endorsement, or public-release authorization for that source or for repository code. A release owner must resolve applicable rights and name the actual terms before external distribution.
- Contributor submissions retain whatever rights their authors hold until a separate, explicit reuse agreement records otherwise. Attribution choices in `FLOW.md` are operational preferences, not a transfer of copyright.

## Release record, 21 September 2026

Public release of this packet was approved by the project owner on 21 September 2026 ("You're approved/allowed to use the contributor pack in any way you see fit"). Released files: the exact list above plus this record, `LICENSE-TEXT` (CC BY 4.0 for text and data), `LICENSE-CODE` (MIT for `check_packet.py` and `tests/`), `.github/ISSUE_TEMPLATE/contributor-report.md` as the submission route, and a three-line `.gitignore` (`__pycache__/`, `*.pyc`, `.DS_Store`). `OUTREACH_UNSENT.md` and `RESULTS.md` remain internal. Changes from the local review copy: the maintainer command in `README.md` no longer carries a local path; the submission route is named; task status fields read `released`; a "Who runs this" paragraph carries the project's maturity statement and links The Accord.

Repository: https://github.com/Good-Work-Movement/governance-lab-starter (public, pushed 21 September 2026). The Lab recorded the decision the same day (commit a8f1714 in the private archive); the only correction requested was this inventory line for `.gitignore`.

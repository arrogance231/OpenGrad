# OpenGrad Phase 0 Bootstrap Report

## 1. What was created

A model-agnostic Python package, registries, JSON Schema experiment contract, canonical tool-conversation types, source-adapter fixtures, contamination fixture scanner, provenance records, optional integration boundaries, documentation, templates, CI, and tests.

## 2. Repository tree

See `docs/architecture/repository.md` for the maintained map.

## 3. Design decisions

Canonical tool conversations are separated from model-native renderers. Training methods are interfaces/configuration namespaces only. Run records preserve failed and rejected work. Large artifacts are ignored rather than committed.

## 4. Dataset registry status

All six requested primary tool-calling sources and APIGen-MT-5k are registered. Counts, licenses, revisions, hashes, and retained counts remain explicitly pending authoritative retrieval/audit; no corpus was downloaded.

## 5. Benchmark registry status

BFCL V4, When2Call, tau-bench/tau2, ToolSandbox, MCPMark Verified, Toolathlon, and regression slots are registered. Canonical sources and verified bibliographic metadata are recorded where available; evaluator release/commit fields remain per-run fields. No scores exist.

## 6. Paper/research infrastructure

`docs/references/papers.yaml` contains 21 field-level records. Verification used arXiv Atom, OpenAlex, official GitHub APIs/raw files, and Hugging Face dataset APIs/pages directly. OpenPapers was inspected at commit `5174637cacdd83dcfaf147c93b11f2633f944d7e`; Firecrawl was not required. Unresolved fields retain null/status/check-source metadata rather than being invented.

## 7. OpenPapers

Optional workflow documented in `docs/research/OPENPAPERS.md`; no runtime dependency or secrets.

## 8. OpenWeights

Documentation and interoperability result schema are present under `docs/openweights/` and `integrations/openweights/`; OpenWeights was not modified.

## 9. Tests executed

Verified from the final checkout: `uv run ruff check .` passed; `uv run ruff format --check .` passed (66 files); `uv run pytest` passed (4 tests); `uv run opengrad-validate` passed; `uv run mypy src` passed; and `git diff --check` passed.

## 10. Remaining Phase 0 limitations

Processed dataset hashes and retained-after-filtering counts are unavailable because corpus materialization and preparation intentionally belong to Phase 2. Per-split row counts unavailable through the checked metadata endpoints remain explicitly unresolved. Benchmark evaluator commits, runtime versions, and hardware measurements are execution-time fields. Baseline scores, OpenGrad-trained checkpoints, exports, device benchmarks, actual contamination scans, and speculative decoding remain unavailable because their phases have not begun.

## 11. Prerequisites for first experiment

Resolve any remaining dataset-specific terms/revisions; audit and hash source manifests; select baseline models and native protocols; freeze evaluator versions; define hardware/software capture; approve a baseline-only Phase 1 task.

## 12. Recommended next research action

After explicit authorization for Phase 1, reproduce a frozen, untouched baseline on a credentialed evaluation environment before preparing any training mixture.

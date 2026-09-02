# Phase 0.5 — Pre-Experiment Validation Report

## 1. Completed work

Implemented CPU-safe canonical tool schema validation, six source adapter boundaries with fixtures, model-family renderer seams, strict tool-call parser states, synthetic contamination methods, benchmark mock harnesses, normalized evaluation results, taxonomy mapping, experiment definition, lineage and stage gates, data statistics and mixture analysis, configuration validation, report generation, environment capture, CLI preflight, and Phase 1/2 protocols.

## 2. Remaining unresolved metadata

The bibliography and dataset registry now use field-level `VERIFIED`, `PARTIAL`, or `UNRESOLVED` records with checked sources. Remaining unresolved items are explicitly limited to metadata not established by the checked primary sources: the canonical identity of the STAR queue entry, Toolathlon canonical identity/release, some LoopTool paper metadata, some benchmark evaluator revisions, and per-split counts unavailable without materialization or authoritative published counts.

## 3. Benchmark harness status

CPU mock smoke harnesses accept deterministic predictions and emit `SMOKE_TEST_ONLY` result envelopes for BFCL, When2Call, τ-bench/τ², ToolSandbox, MCPMark, and Toolathlon. No real model or benchmark score was produced. BFCL and τ-bench repository default revisions are pinned in `registry/benchmarks.yaml`; other defaults remain explicitly unresolved where no canonical repository was established.

## 4. Dataset-adapter status

Fixture adapters exist for xLAM, When2Call, ToolACE, BUTTON, LoopTool, and Glaive. They preserve source identity/split metadata, reject malformed records, and do not materialize full datasets.

## 5. Parser/schema status

Canonical conversations support system/user/assistant/tool roles, multiple and parallel calls, call IDs, results, sequential turns, no-call/clarification/impossible-tool responses, and strict rejection. Parser output distinguishes `RAW_VALID` and `INVALID`; no automatic repair is performed.

## 6. Contamination-tool status

Synthetic tests cover normalized exact hashes, canonical JSON signatures, n-gram Jaccard, edit similarity, and MinHash. Real corpora were not scanned. Semantic embeddings remain optional and unimplemented.

## 7. Experiment registry status

`tool_calling/qwen35_2b/baseline` exists as `PLANNED` only. Model revision and generation settings remain placeholders until Phase 1 authorization. Lineage and scientific stage gates are unit-tested.

## 8. Tests executed

Final verification passed: Ruff, format check, pytest (29 passed), registry validation, mypy, CLI preflight, six benchmark mock smoke harnesses, and diff checks. All are CPU-only and GPU-free.

## 9. Known limitations

No GPU, model inference, large checkpoint download, full benchmark run, training, dataset materialization, real contamination scan, GGUF/ExecuTorch export, or speculative decoding was performed. Those are later-phase activities.

## 10. Tasks requiring GPU access

Future Qwen3.5-2B baseline inference and full benchmark reproduction; training/post-training; teacher/student distillation; GPU runtime comparisons; and any accelerator-specific throughput work.

## 11. CPU-only but intentionally deferred

Further primary-source reading for unresolved STAR/Toolathlon identities, exact per-split metadata where not publicly exposed, evaluator-specific adapters beyond the generic smoke contract, model-native renderer validation against exact tokenizer revisions, semantic contamination embeddings, and additional benchmark revision pinning when canonical repositories are identified.

## 12. Readiness decision

READY_FOR_PHASE_1

This means the repository preflight and CPU validation infrastructure pass. It does not authorize Phase 1 or begin any model work. Phase 1 still requires explicit authorization and must follow `docs/experiments/BASELINE_REPRODUCTION_PROTOCOL.md`.

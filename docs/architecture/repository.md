# Repository architecture

OpenGrad has four boundaries: registries (declarative identity and versions), canonical data (source-independent semantics), adapters/renderers (source and model protocol boundaries), and evidence (runs, reports, artifacts). Training and inference implementations are intentionally absent from Phase 0.

Large data/checkpoints live outside Git and are referenced by immutable revisions and hashes. `results/registry.jsonl` is an append-only index for future records; failed runs are retained.

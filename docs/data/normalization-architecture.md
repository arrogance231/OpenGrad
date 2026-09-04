# Normalization architecture

OpenGrad deliberately separates three transformations:

```text
A. source normalization: native dataset format -> canonical semantic IR
B. research normalization: IR -> validation, quality, dedup, contamination, behavior, mixture
C. model materialization: selected IR -> exact checkpoint tokenizer/chat-template representation
```

The semantic IR describes what happened: roles, typed tool definitions, calls, call IDs, observations, ordering, behavior, provenance, and source-only features. The model renderer describes how one exact checkpoint serializes those semantics. This permits identical IDs, splits, behavioral mixtures, and canonical hashes to be compared across registered models while changing only renderer and training variables.

Laptop/CPU stage: download, parse, canonicalize, validate, deduplicate, contamination audit, behavioral audit, render, token statistics, fixtures, and reports.

Datacenter GPU stage: baseline inference, SFT, evaluation, conditional preference experiments, distillation, runtime benchmarking, and speculative/MTP experiments.

Historical Phase 0/0.5 reports retain their original fixture-only claims; this document records the subsequent normalization implementation without rewriting history.

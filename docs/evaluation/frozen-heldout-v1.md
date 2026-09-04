# Frozen held-out evaluation contract

`behavioral-heldout-v1.manifest.json` is the frozen pre-GPU evaluation set. It contains materialized evaluation-only record counts and content hashes, freezes the renderer identity and contamination boundary, and contains no model scores.

- model revision: `15852e8c16360a2fea060d615a32b45270f8a8fc`
- renderer: `qwen3_5_2b_v1`
- template hash: `273d8e0e683b885071fb17e08d71e5f2a5ddfb5309756181681de4f5a1822d80`
- status: `FROZEN_PRE_GPU`
- materialized items and content hashes: MCQ 3,652; LLM judge 300

The manifest is independently generated from evaluation-only entities and prompts disjoint from training mixtures, with content hashes frozen before baseline execution. The JSON contract is `registry/evaluation_manifest.schema.json`.

# OpenGrad

OpenGrad is research infrastructure for empirical evaluation of capability–efficiency tradeoffs in post-trained small open-weight language models. It is designed as an open record of what changes models, why, what it costs, what it breaks, and whether findings reproduce—not as a collection of successful fine-tunes.

**Status: Phase 0 — repository and research infrastructure. No OpenGrad training results exist yet. No model has been trained, no checkpoint has been modified, and speculative decoding has not been implemented.**

## Research tracks

- **Capability / post-training:** initially reliable tool use—call, no-call, clarification, impossible requests, selection, arguments, parallelism, dependencies, observations, and multi-turn state—while checking ordinary instruction-following regressions.
- **Inference / systems efficiency:** future GGUF, llama.cpp, ExecuTorch, quantization, CPU/ARM/mobile measurements, and speculative-decoding studies. This track is separate from behavioral claims and will not be assumed to improve them.

The project is model-agnostic and can compare Qwen, LFM, Gemma, Llama, Phi, SmolLM, and future small open-weight families through native model adapters.

## Repository map

- `registry/`: versioned datasets, benchmarks, models, runtimes, hardware, and experiment schema.
- `src/opengrad/`: lightweight canonical data, registry validation, contamination fixtures, and provenance types.
- `configs/`: future model-native, data, training, evaluation, and inference configurations.
- `experiments/`, `reports/`, `results/`: planned runs and evidence; failed runs remain part of history.
- `docs/`: architecture, methodology, OpenPapers/OpenWeights boundaries, and benchmark notes.
- `hf/`: model, dataset, and experiment-card templates.

## Scientific policy

Every future run has a stable `run_id`, parent checkpoint, exact revisions, dataset manifest/hash, benchmark versions, hardware/software provenance, metrics, regressions, failure analysis, and an evidence-based decision. Loss reduction or a few prompt examples are not evidence of improvement. Results are never silently compared across materially different benchmark versions.

The initial tool registry records xLAM/APIGen Function Calling 60k, NVIDIA When2Call, ToolACE, BUTTON/BUTTONInstruct, LoopTool-23k, and Glaive Function Calling v2. `Salesforce/APIGen-MT-5k` is explicitly excluded from the clean default and can only appear under `contaminated/apigen-mt`. Planned mixture percentages are hypotheses, not defaults that imply optimality.

## Reproducibility

Use `uv sync --extra dev`, then `uv run pytest`. Registry validation is credential-free and does not download models or datasets. Optional integrations are intentionally separated because PyTorch, Transformers, TRL, vLLM/SGLang, llama.cpp, and ExecuTorch may require incompatible environments.

## Prior work

Small-Mind Companion, SchemaForge, and `arrochi112/onebee-gf-distill-v1` are related maintainer work, not OpenGrad results. See `docs/research/prior-work.md`.

## Roadmap and citation

See `ROADMAP.md` and `BOOTSTRAP_REPORT.md`. OpenGrad source code is licensed under Apache-2.0; third-party assets retain their own terms.

# OpenGrad

OpenGrad is an open research repository for measuring capability–efficiency tradeoffs in post-trained small open-weight language models.

The project treats model changes as experiments, not as presumed improvements. Each result should preserve the model and dataset revisions, benchmark versions, hardware and software environment, regressions, failure analysis, and reproduction evidence.

**Current status: Phase 0.5 — CPU-only pre-experiment validation. No OpenGrad training, model inference, benchmark evaluation, or published research results exist yet.**

## Research tracks

### Capability and post-training

The first planned study concerns reliable tool use in small models:

- deciding when to call a tool, answer directly, clarify, or report that a request is unsupported;
- selecting tools and producing valid, grounded arguments;
- handling parallel calls, sequential dependencies, observations, failures, and multi-turn state;
- measuring ordinary instruction-following regressions alongside tool-use performance.

### Inference and systems efficiency

A separate track will study quantization, GGUF, llama.cpp, ExecuTorch, CPU and ARM inference, mobile deployment, and eventually speculative decoding. Capability and efficiency are evaluated separately before they are considered jointly.

OpenGrad is model-agnostic. Model-family adapters are designed for Qwen, LFM, Gemma, Llama, Phi, SmolLM, and future small open-weight models without imposing one universal tool protocol.

## Quick start

Requirements: Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --extra dev
uv run opengrad-validate
uv run opengrad-preflight
uv run pytest
```

These commands validate registries and CPU-only fixtures. They do not download models or datasets and do not require a GPU.

## Repository layout

- `registry/` — versioned dataset, benchmark, model, runtime, hardware, provenance, and experiment contracts.
- `src/opengrad/` — canonical data, adapters, parsers, contamination tooling, evaluation schemas, lineage, and reporting utilities.
- `configs/` — model, data, evaluation, training, inference, and planned experiment configurations.
- `docs/` — architecture, methodology, reproducibility, dataset protocols, benchmark notes, and integration boundaries.
- `experiments/`, `reports/`, `results/` — append-only research records and report namespaces; no completed OpenGrad results are present yet.
- `hf/` — model-card, dataset-card, and experiment-report templates.

## Research safeguards

- Source data are normalized into a canonical representation before model-specific rendering.
- Evaluation-only and preference-only splits are excluded from clean training configurations.
- `Salesforce/APIGen-MT-5k` is excluded from the clean default because of potential overlap with τ-bench-style tasks.
- Failed, rejected, and negative experiments remain part of the scientific record.
- Benchmark revisions, dataset revisions, and checkpoint lineage are recorded explicitly.
- CI uses small synthetic fixtures and does not require credentials, large checkpoints, or accelerators.

See [the roadmap](ROADMAP.md), [the Phase 0.5 report](PRE_EXPERIMENT_REPORT.md), and [the reproducibility guide](docs/research/reproducibility.md) for details.

## Related projects

- [OpenPapers](https://github.com/arrogance231/openpapers) — optional literature discovery and scholarly provenance infrastructure.
- [OpenWeights](https://github.com/alpharomercoma/openweights) — separate downstream environment for future practical device-side evaluation.
- [Small-Mind Companion](https://github.com/arrogance231/small-mind-companion) and [SchemaForge](https://github.com/arrogance231/SchemaForge) — related maintainer projects, not OpenGrad results.

## Contributing

Useful contributions include reproductions, alternative seeds, new model-family adapters, dataset audits, benchmark discrepancy reports, hardware and mobile measurements, quantization studies, inference implementations, and negative results.

Start with [CONTRIBUTING.md](CONTRIBUTING.md) and the templates under `docs/contributing/`. Contributions should include exact revisions, configuration, provenance, observed regressions, and limitations.

## License and citation

OpenGrad source code and documentation are licensed under [Apache-2.0](LICENSE). Third-party datasets, models, benchmark assets, papers, and imported code retain their own terms.

See [CITATION.cff](CITATION.cff) for citation metadata. A formal release DOI has not been assigned.

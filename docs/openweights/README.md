# OpenWeights boundary

OpenWeights ([repository](https://github.com/alpharomercoma/openweights)) is an independent downstream execution environment for practical device-side studies, not an OpenGrad dependency. Its deployment observations motivate OpenGrad's controlled reliability questions; they remain external observations until independently reproduced by an OpenGrad baseline.

OpenGrad separates tool-call syntax from tool-use policy and agent task completion. OpenGrad turns phenomena such as under-/over-calling, catalogue sensitivity, observation handling, and structured-output failures into canonical behaviors, deterministic evaluations, and later controlled interventions. It does not copy OpenWeights prompts into training or claim an official OpenWeights benchmark. The planned held-out family is documented in `docs/evaluation/deployment-derived-routing.md`.

Capability data and speculative/MTP continuation data remain separate objectives. Future workload profiles may describe ordinary conversation, reasoning, tool-decision turns, structured calls/JSON, observations, short and long responses, code, long prefill/short decode, and multi-turn agents. OpenWeights supports downstream GGUF/llama.cpp and ExecuTorch deployment paths; OpenGrad records the evidence boundary for future transfer studies.

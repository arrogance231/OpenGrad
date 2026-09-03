# Deployment-derived routing evaluation

Planned held-out evaluation family motivated by failure phenomena observed in the independent [OpenWeights](https://github.com/alpharomercoma/openweights) deployment work. OpenGrad will derive phenomena—not copy benchmark prompts—and generate disjoint prompts/entities from training and baseline fixtures.

Planned coverage: fresh-information must-call, static-knowledge no-call, missing arguments, irrelevant and near-match catalogues, unavailable tools, ambiguous entities, multiple plausible tools, unsupported requests, observation-follow-up and stop decisions, tool failure, and small/large catalogues. It will record contamination lineage and catalogue metadata.

This is an OpenGrad planned evaluation, not an official OpenWeights benchmark and not an OpenGrad result. It will be evaluated as Layer 3 after deterministic behavioral tests and external benchmark transfer (Layers 1 and 2). The primary decision matrix includes CALL, ANSWER, CLARIFY, and UNSUPPORTED, with directional routing and structured-agent metrics.

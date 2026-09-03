# Methodology revision record

Date: 2026-09-03
Status: IMPLEMENTED infrastructure / SCHEMA-READY methodology; no training or baseline inference performed.

## Change

OLD: source-manifest-centric candidate mixture, where dataset brands and proposed source percentages were the primary abstraction.

NEW: dual-axis source provenance plus behavioral capability model. M0 retains the old source-oriented hypothesis as a control. M1 is a behaviorally balanced hypothesis. M2 is a deterministic, baseline-residual-driven strategy that cannot produce weights until an executed baseline supplies sufficient evidence.

## Rationale and evidence boundary

OpenWeights deployment observations showed that tool-capable small models can fail in different directions, including over-calling versus under-calling. This makes one universal call-heavy recipe scientifically questionable. Those observations motivate OpenGrad's hypotheses; they are not OpenGrad baselines or results and have not been reproduced here.

OpenGrad has not established that residual-driven mixtures outperform generic mixtures. That is an experimental hypothesis to test with B0/M0/M1/M2 under matched evaluation conditions.

## Consequences

Canonical examples retain source, split, revision, contamination, behavior labels, label uncertainty, catalogue conditions, retention eligibility, and counterfactual identity. Coverage reports measure composition rather than repeating planned percentages. Historical reports remain historical and link to the new method.

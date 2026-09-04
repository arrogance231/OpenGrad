# Repository architecture

OpenGrad is a provenance-first empirical research repository. The current pre-GPU pipeline has four boundaries: registries (declarative identity and versions), canonical data (source-independent semantics), adapters/renderers (source and model protocol boundaries), and evidence (manifests, reports, runs, and artifacts).

## Current data flow

```text
upstream dataset
    -> source-specific adapter
    -> canonical semantic IR
    -> semantic validation and quarantine
    -> quality classification and deduplication
    -> contamination boundary
    -> behavioral metadata
    -> clean SFT candidate index
    -> exact-model tokenizer/chat-template renderer
    -> training or evaluation artifact
```

Universalize the meaning; specialize the representation. Canonical records remain model-independent. Qwen rendering is a separate exact-checkpoint operation using the pinned tokenizer/template contract.

## Canonical boundaries

`CanonicalSFTExample`, `CanonicalPreferenceExample`, and `CanonicalEvaluationExample` are separate contracts. Preference records preserve context, chosen, and rejected responses; rejected responses never silently become SFT targets. Evaluation records preserve expected decisions and candidates in an evaluation-only namespace; they never silently enter training.

## Current evidence boundary

The accessible pinned sources are normalized, audited, and rendered into local ignored artifacts. Manifests preserve source revisions, adapter versions, checksums, canonical schema, behavioral taxonomy, and retained counts. The frozen held-out evaluation is separate from training. Large data and rendered files remain outside Git; tracked schemas, configurations, small fixtures, and summary reports define the reproducible interface.

The first empirical model action is B0: unmodified `Qwen/Qwen3.5-2B` inference against the frozen held-out evaluation. No model-quality result, training result, or speculative-decoding result exists yet.

# Hugging Face dataset publication

OpenGrad uses a two-repository publication boundary.

GitHub is the canonical home for source code, schemas, manifests, provenance, audits, reproduction commands, and experiment definitions. Hugging Face is the distribution home for large canonical dataset artifacts, dataset cards, source attribution, release manifests, and checksums.

## Current release definition

`OpenGrad ToolPolicy Canonical v1` is `CANONICAL_DATASET_PUBLISHED` at Hub commit `bb295d8a4ad64f7e8161044ad2fa34f873ede418`. The public payload contains the five previously cleared sources plus 59,370 xLAM/APIGen normalized records under CC BY 4.0 with attribution and modification disclosure. The xLAM upstream access gate is not reproduced downstream. The exact publication record is `reports/releases/toolpolicy-canonical-v1-publication.json`.

The tracked release config is `configs/releases/toolpolicy_canonical_v1.yaml`. The tracked dataset-card, licensing, and citation inputs are under `release/huggingface/toolpolicy-canonical-v1/`. Generated staging output belongs under `.release/` and is ignored.

## Release scope

The release builder reads source manifests rather than hard-coding record counts. It writes ordinary Parquet with source-aware columns, including `source_dataset`, `source_record_id`, `source_revision`, `canonical_hash`, quality state, behavior metadata, and canonical tools/messages/metadata.

The intended source scope is xLAM, BUTTON, ToolACE, LoopTool, Glaive Function Calling v2, and When2Call SFT. When2Call preference, MCQ, and LLM-judge artifacts are explicitly excluded. The frozen 3,952-record evaluation namespace is never embedded in the training/candidate release. Qwen-rendered text is also excluded; model-specific rendering remains a separate experiment artifact.

The release includes xLAM under CC BY 4.0 as a normalized derivative, with attribution, APIGen citation, and modification disclosure. Its upstream access mode is gated, but downstream redistribution is explicitly permitted with attribution; the OpenGrad release is public and does not reproduce the upstream gate.

## Commands

Build local staging without uploading:

`uv run opengrad-data build-hf-release --release-config configs/releases/toolpolicy_canonical_v1.yaml --output .release/hf/toolpolicy-canonical-v1`

Validate staging:

`uv run opengrad-data validate-release --input .release/hf/toolpolicy-canonical-v1`

These commands do not invoke the Hugging Face upload CLI.

## Versioning

Release meaning is immutable. PATCH releases correct metadata or provenance without changing record semantics. MINOR releases add compatible sources/configurations or clearly documented compatible corrections. MAJOR releases change canonical schema or dataset meaning. Every experiment must pin the exact Hub revision and record the release manifest hash.

## Experiment lineage

Future model provenance must identify the upstream source, the exact OpenGrad canonical release revision, the experiment-specific mixture and config, experiment ID, checkpoint, and evaluation report. “Trained on OpenGrad” alone is insufficient.

## Upload gate

Before a future release update, recheck current upstream licenses, dataset cards, repository terms, gated conditions, attribution, and citation requirements. Validate the generated manifest, Parquet payloads, card, citations, license audit, checksums, counts, and absence of evaluation/preference leakage. The v1.0.0 publication is recorded at Hub commit `bb295d8a4ad64f7e8161044ad2fa34f873ede418`.

# Source redistribution audit for OpenGrad ToolPolicy Canonical v1

Audit scope: publication preparation only. This is a provenance and metadata audit, not legal advice. The release builder fails closed for sources whose upstream distribution boundary is not clearly cleared.

| Source | Upstream source | Pinned revision | Observed license metadata | Distribution status | Publication treatment |
|---|---|---|---|---|---|
| xLAM | https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k | `26d14ebfe18b1f7b524bd39b404b50af5dc97866` | HF card reports CC-BY-4.0; gated access is enabled | GATED_SOURCE_REVIEW_REQUIRED | Excluded by default until accepted gated terms are reviewed for redistribution of normalized rows |
| BUTTON | https://github.com/PKU-Baichuan-MLSystemLab/BUTTON | `47cb720ed223b249a2f1d0a3faf1cb1eb7175622` | GitHub repository metadata reports CC-BY-4.0 | REDISTRIBUTION_WITH_ATTRIBUTION | Eligible with attribution; retain upstream notices and dataset citation |
| ToolACE | https://huggingface.co/datasets/Team-ACE/ToolACE | `6bda777c88d21e5a204703c1ee45597a8fa4f734` | HF dataset metadata reports Apache-2.0 | REDISTRIBUTION_WITH_ATTRIBUTION | Eligible with attribution; verify card terms again immediately before upload |
| LoopTool-23k | https://huggingface.co/datasets/zhangkangning/LoopTool-23k | `b6c572d442ed4f2177f23645d8e9a77522e712c3` | HF dataset metadata reports Apache-2.0 | REDISTRIBUTION_WITH_ATTRIBUTION | Eligible with attribution; preserve possible derivation warning |
| Glaive Function Calling v2 | https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2 | `e7f4b6456019f5d8bcb991ef0dd67d8ff23221ac` | HF dataset metadata reports Apache-2.0 | REDISTRIBUTION_WITH_ATTRIBUTION | Eligible with attribution; verify card terms again immediately before upload |
| When2Call | https://huggingface.co/datasets/nvidia/When2Call and https://github.com/NVIDIA/When2Call | `0582f7749df63a96fdc3070932e83e72396ace53` | HF dataset metadata reports CC-BY-4.0 | REDISTRIBUTION_WITH_ATTRIBUTION | Eligible with attribution; keep SFT, preference, and evaluation configurations separate |

## xLAM boundary

The xLAM file was accessed through an accepted gated account and normalized locally. That access does not by itself establish permission to redistribute the normalized derivative corpus. Until the current gated terms are reviewed and cleared, the release configuration excludes xLAM and records the exclusion in the generated release manifest. No mirror or alternate source is used to bypass the gate.

## Mixed-license policy

The Apache-2.0 license in the OpenGrad repository applies to OpenGrad source code, not automatically to upstream datasets. The Hugging Face dataset card must retain this per-source table, upstream links, revisions, citations, and required attribution. A single top-level license field must not be used to imply relicensing of every upstream component.

## Recheck requirement

Upstream cards, repository terms, gated conditions, and redistribution status must be rechecked immediately before any future update. The v1.0.0 release was published only after this audit; its public payload excludes xLAM pending gated redistribution review.

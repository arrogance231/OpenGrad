# OpenGrad normalization sources

Status: CURRENT REFERENCE / FULL ACCESSIBLE CORPORA MATERIALIZED. Historical parser progression and exclusions remain in `reports/data-normalization-v1.md`.

OpenGrad uses three separate transformations:

```text
source-specific native record -> canonical semantic IR -> research normalization -> exact-model rendering
```

The canonical IR is model-independent. Native delimiters, source roles, serialized JSON, source reasoning, and lineage are retained in `metadata.source_features`; raw records remain outside the repository under `data/raw/`.

Pinned dataset snapshots currently recorded by the repository registry:

| Adapter | Official source | Registry snapshot | Native shape |
|---|---|---|---|
| xLAM | `Salesforce/xlam-function-calling-60k` | `26d14ebfe18b1f7b524bd39b404b50af5dc97866` | `id/query/tools/answers`, tools and answers may be JSON strings |
| When2Call | `nvidia/When2Call` | `0582f7749df63a96fdc3070932e83e72396ace53` | split-specific SFT/preference/evaluation records; tool calls use `<TOOLCALL>` |
| ToolACE | `Team-ACE/ToolACE` | `6bda777c88d21e5a204703c1ee45597a8fa4f734` | `system/conversations`, entries use `from/value` |
| BUTTON | official Git repository | `47cb720ed223b249a2f1d0a3faf1cb1eb7175622` | message sequences; `<tool>`, `<call>`, `<final>` text markers |
| LoopTool | `zhangkangning/LoopTool-23k` | `b6c572d442ed4f2177f23645d8e9a77522e712c3` | `instruction/input/output`; reported ToolACE-derived lineage is preserved |
| Glaive v2 | `glaiveai/glaive-function-calling-v2` | `e7f4b6456019f5d8bcb991ef0dd67d8ff23221ac` | `system/chat`, `USER:`, `ASSISTANT:`, `<functioncall>`, `FUNCTION RESPONSE:` |

The accessible pinned sources are materialized and audited. xLAM has 59,370 valid records, BUTTON 7,941, ToolACE 11,190, LoopTool 20,827, Glaive 99,794, and When2Call SFT 14,829. The separate When2Call preference and evaluation artifacts are also materialized. xLAM and BUTTON are no longer blocked; BUTTON's 59 duplicate-tool failures and LoopTool's renderer exclusions remain explicit.

The repository makes no official-paper or official-recipe claim for Glaive v2; `papers: []` is intentional.

Qwen renderer provenance:

- exact checkpoint: `Qwen/Qwen3.5-2B`
- registry revision: `15852e8c16360a2fea060d615a32b45270f8a8fc`
- implementation: `src/opengrad/data/renderers.py`, `qwen3_5_2b_v1`
- behavior: lazy `AutoTokenizer.from_pretrained(..., revision=...)` and `apply_chat_template`; weights are never instantiated
- template hash: recorded at render time because it is an artifact property, not a hand-authored constant

Primary model references are the exact tokenizer artifact at the pinned checkpoint, Qwen-Agent's Qwen3.5 example, and Qwen's function-call documentation. External training references are not OpenGrad configurations.

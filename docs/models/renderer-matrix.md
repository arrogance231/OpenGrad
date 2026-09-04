# Model renderer matrix

| Exact checkpoint | Revision pinned | Template inspected | Renderer implemented | Snapshot tested | Training validated |
|---|---|---|---|---|---|
| `Qwen/Qwen3.5-2B` | YES: `15852e8c16360a2fea060d615a32b45270f8a8fc` | MEASURED: pinned tokenizer hash `273d8e0e683b885071fb17e08d71e5f2a5ddfb5309756181681de4f5a1822d80` | IMPLEMENTED | COMPLETE: eight golden fixtures | PREPARED; no training run |

Only registered exact checkpoints receive renderers. The canonical layer does not contain Qwen syntax. Rendering is lazy and uses tokenizer `apply_chat_template`; neural network weights are not loaded. The full SFT render audit produced 210,874 candidates; 3,077 canonical-valid LoopTool records remain explicit exclusions because the pinned template requires a user query.

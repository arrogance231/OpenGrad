# External training reference recipes

Status: RESEARCHED_ONLY. These values are references, not OpenGrad configurations. No SFT, preference optimization, GRPO, or distillation was run in this normalization phase.

| Source | Method / data | Reported details | Unknown / boundary |
|---|---|---|---|
| Salesforce xLAM ActionStudio | full fine-tuning, LoRA, NF4+LoRA examples | official scripts and conversion guide are the authority | exact settings vary by example; extract per pinned script before reuse |
| NVIDIA When2Call | SFT and preference generation; LM-Eval prompt variants | repository distinguishes `train_sft`, `train_pref`, `mcq`, `llm_judge` | OpenGrad must not convert preference/evaluation rows into SFT |
| ToolACE paper / model card | SFT/LoRA reference recipe | paper is the authority for reported setup | unreported fields remain UNKNOWN; not an OpenGrad config |
| BUTTON paper/repository | training methodology | `OFFICIAL_EXECUTABLE_TRAINING_CONFIG: NOT FOUND` unless a pinned repository file is located | do not infer missing optimizer, LR, or precision |
| LoopTool repository | GRPO/Qwen conversion and training scripts; GCP/JGLV/EDDE | `conversation_transform_grpo_qwen.py`, `train_grpo_qwen.sh` are reference artifacts | GRPO is not OpenGrad's initial SFT study |
| Glaive v2 | official dataset only | `OFFICIAL_EXECUTABLE_TRAINING_CONFIG: NOT FOUND`; no authoritative paper identified here | no community recipe is represented as official |
| Qwen3.5 | ms-swift best-practice documentation; Qwen-Agent/runtime docs; LLaMA-Factory support | useful references for template, LoRA, bf16, packing, and framework behavior | exact OpenGrad training config is intentionally undecided |

Required future extraction fields are: source, repository/paper, base model, method, dataset, epochs, learning rate, batch size, sequence length, optimizer, scheduler, warmup, LoRA rank/alpha/targets, precision, hardware, evaluation, and `UNKNOWN` for absent values.

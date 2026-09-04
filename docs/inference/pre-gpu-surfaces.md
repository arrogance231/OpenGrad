# Pre-GPU configuration surfaces

All accelerator work remains unstarted. `configs/hardware/gpu_preflight_v1.yaml` is a schema-valid `NOT_RUN` record; it is not a claim that any GPU, driver, CUDA, ROCm, runtime, or quantization path works.

A future preflight must record requested and observed device counts, VRAM, driver/runtime versions, provider (`nvidia` or `amd`), and a compatibility result with its basis. `UNKNOWN`, `NOT_TESTED`, and `INCOMPATIBLE` must not be collapsed into support. The contract is `registry/gpu_preflight.schema.json`.

## Reserved runtime/component references

`registry/runtime_components.yaml` records upstream references only:

- NVIDIA ModelOpt: quantization reference; NVIDIA `NOT_TESTED`, AMD/CPU `UNKNOWN`.
- vLLM Speculators: speculative-decoding reference; NVIDIA and AMD `NOT_TESTED`.
- DSpark: inference-runtime reference; NVIDIA and AMD `NOT_TESTED`.

These entries provide provenance and an explicit compatibility matrix. They do not install dependencies, download weights, run inference, or establish support. Their machine-readable contract is `registry/runtime_components.schema.json`; `registry/runtimes.yaml` retains the runtime-level index.

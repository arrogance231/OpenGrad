# Baseline reproduction protocol

This document is a future Phase 1 protocol. It is not executed in Phase 0.5.

1. Acquire accelerator and record hardware/software environment.
2. Fetch the exact Qwen3.5-2B model revision and record its license.
3. Validate native chat template and tool parser.
4. Run a tiny inference sanity check, then benchmark mini-smoke.
5. Run full BFCL baseline, When2Call baseline, τ² baseline, and general-regression baseline.
6. Compare against published/reference results with exact revisions and generation settings.
7. Investigate discrepancies and accept the baseline only after the reproduction gate.

No model revision, inference, or benchmark execution is selected or performed by this Phase 0.5 document.

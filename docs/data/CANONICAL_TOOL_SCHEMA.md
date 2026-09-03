# Canonical tool schema

A conversation retains backwards-compatible `id`, `source`, `tools`, `messages`, and provenance `metadata.split`. The source axis is additionally represented in `metadata.source` with `dataset_id`, `revision`, and `original_split`.

The optional behavioral axis uses `metadata.behavior`: one canonical decision (`CALL`, `ANSWER`, `CLARIFY`, or `UNSUPPORTED`), capability IDs from `registry/tool_behaviors.yaml`, and a confidence state (`known`, `derived`, `heuristic`, or `unknown`). Optional `tool_context`, `interaction`, `training`, and `counterfactual` metadata record catalogue conditions, eligibility, and decision-boundary groups without altering the conversation protocol.

Tools require unique `name`; messages use only `system`, `user`, `assistant`, or `tool`. Assistant messages may contain zero or more `{id,name,arguments}` calls. Tool messages require `tool_call_id`.

Ordering is preserved. Parallel calls are represented as multiple calls in one assistant message; sequential calls are represented by later assistant messages after tool observations. No-call, clarification, and unsupported responses are ordinary assistant content with zero calls. Unknown tools, duplicate IDs, missing fields, non-object arguments, invalid roles, unknown behavior IDs, invalid catalogue counts, and malformed counterfactual metadata fail validation; no silent repair occurs.

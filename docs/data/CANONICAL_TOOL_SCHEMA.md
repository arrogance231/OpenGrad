# Canonical tool schema

A conversation has `id`, `source`, `tools`, `messages`, and provenance `metadata.split`. Tools require unique `name`; messages use only `system`, `user`, `assistant`, or `tool`. Assistant messages may contain zero or more `{id,name,arguments}` calls. Tool messages require `tool_call_id`.

Ordering is preserved. Parallel calls are represented as multiple calls in one assistant message; sequential calls are represented by later assistant messages after tool observations. No-call, clarification, and impossible-tool responses are ordinary assistant content with zero calls. Unknown tools, duplicate IDs, missing fields, non-object arguments, and invalid roles fail validation; no silent repair occurs.

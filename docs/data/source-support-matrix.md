# Source support matrix

| Dataset | Raw adapter | Canonical conversion | SFT | Preference | Multi-turn | Parallel | Tool results | Behavioral labels | Full materialization |
|---|---|---|---|---|---|---|---|---|---|
| xLAM | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | NOT_APPLICABLE | source-dependent | source-dependent | source-dependent | IMPLEMENTED | FULL_DATA_VALIDATED |
| When2Call | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | PARTIAL (separate policy required) | IMPLEMENTED | UNKNOWN | source-dependent | IMPLEMENTED | FULL_DATA_VALIDATED |
| ToolACE | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | NOT_APPLICABLE | IMPLEMENTED | source-dependent | IMPLEMENTED | IMPLEMENTED | FULL_DATA_VALIDATED |
| BUTTON | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | NOT_APPLICABLE | IMPLEMENTED | source-dependent | source-dependent | IMPLEMENTED | FULL_DATA_VALIDATED |
| LoopTool | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | NOT_APPLICABLE | IMPLEMENTED | UNKNOWN | source-dependent | IMPLEMENTED | FULL_DATA_VALIDATED |
| Glaive v2 | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | NOT_APPLICABLE | IMPLEMENTED | source-dependent | IMPLEMENTED | IMPLEMENTED | FULL_DATA_VALIDATED |

Fixture validation is not dataset validation. The accessible sources above are labeled FULL_DATA_VALIDATED only after the pinned source was streamed, counted, normalized, audited, and checksummed. `source-dependent` and `UNKNOWN` describe capability coverage, not missing materialization.

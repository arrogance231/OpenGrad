# Dataset materialization protocol

Phase 2 will fetch each recorded source revision, preserve source metadata and terms, verify download checksums, adapt records into the canonical schema, validate, deduplicate, scan contamination, filter, calculate retained counts and processed hashes, write a manifest, and freeze the resulting dataset version.

`source_revision` identifies the upstream snapshot now. `processed_dataset_hash` and `retained_after_filtering` cannot exist until materialization and preprocessing have actually occurred; they remain explicitly pending rather than guessed.

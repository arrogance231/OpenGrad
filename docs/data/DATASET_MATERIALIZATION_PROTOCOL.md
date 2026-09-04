# Dataset materialization protocol

The current accessible pinned sources have completed materialization. The protocol preserves source metadata and terms, verifies source checksums, adapts records into the canonical schema, validates, quarantines invalid records, deduplicates, records contamination state, calculates retained counts and processed hashes, writes manifests, and freezes versioned artifacts.

`source_revision` identifies the upstream snapshot. `processed_dataset_hash` and `retained_after_filtering` are recorded in the generated manifests after materialization. Historical pending states are retained in the engineering report where they document earlier work.

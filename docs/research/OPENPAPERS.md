# OpenPapers workflow

OpenPapers is the preferred optional research-reference interface for OpenGrad. At the inspected revision `5174637cacdd83dcfaf147c93b11f2633f944d7e` on `master`, it is an Apache-2.0 MCP server for scholarly retrieval, paper ingestion, and reproducible research workflows.

It provides replaceable adapters for arXiv, Crossref, OpenAlex, Semantic Scholar, GitHub, and Hugging Face; preserves DOI/arXiv/provider identities; discovers citations and implementations; reads bounded paper and repository content without executing it; and records evidence, uncertainty, conflicts, and provider failures. It can run over stdio or Streamable HTTP and uses local SQLite or PostgreSQL/pgvector storage.

## Research workflow

1. Search OpenPapers by title or identifier.
2. Resolve the candidate with a provider-native identifier (`arXiv`, DOI, or OpenAlex ID).
3. Retrieve paper metadata and, when needed, bounded paper sections or implementation files.
4. Record the source URL, revision/blob, locator, and evidence strength in `docs/references/papers.yaml` and an implementation note.
5. Check the canonical paper, project, or dataset page before treating a field as verified. OpenPapers improves provenance and discovery; it does not replace primary-source judgment.
6. Keep recommendations and implementation hypotheses separate from factual evidence.

A citation discovered through OpenPapers enters OpenGrad only after its source identity and relevant fields are recorded. Missing fields remain `null` with an explicit status and a `checked_sources` list.

## Safe local stdio connection

Clone and build OpenPapers separately using its own documented instructions (Node.js >=22.5). In an MCP client, point the server at the built entry point. The repository includes a non-secret conceptual example at `integrations/openpapers/mcp.example.json`:

```json
{
  "servers": {
    "openpapers": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/openpapers/dist/mcp/server.js"]
    }
  }
}
```

Replace the path locally; do not commit absolute machine paths, tokens, or `.env` files. Client configuration keys vary, so follow the client and OpenPapers documentation for the final wrapper.

## Optional boundary

OpenGrad remains reproducible without OpenPapers: direct arXiv, official repository, Hugging Face, Crossref, OpenAlex, or conference sources may be used. OpenPapers is not a Python/runtime dependency, is not required by CI, and does not gate future training or evaluation runs.
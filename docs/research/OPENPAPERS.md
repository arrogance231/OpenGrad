# OpenPapers workflow

OpenPapers is optional literature discovery/evidence infrastructure, not an OpenGrad runtime dependency. An agent conducting a review should use the OpenPapers MCP server to search, retrieve metadata, identify canonical papers, inspect implementations, and record DOI/arXiv IDs and bounded implementation notes.

Configure the MCP client using the OpenPapers project's documented example, replacing its local command/path with the contributor's environment. Do not commit secrets or absolute machine paths. A conceptual configuration belongs in `integrations/openpapers/mcp.example.json`; it is deliberately not executable as-is.

Every claim in OpenGrad documentation should link to a bibliography ID and canonical source. Unknown or conflicting metadata remains marked for verification.

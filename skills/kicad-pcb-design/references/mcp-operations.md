# KiCad MCP operations

## Discovery and lifecycle

Discover current MCP tools and schemas through the server's search or category
inventory. Do not rely on memorized parameter names. Check backend/project state
before editing, open the intended project once, and retain its backend identity.

Save and read back each mutation. If the file changed outside the loaded session,
accept divergence protection: compare both versions, close/reload, and reconcile.
Use an explicit force save only after that comparison. Close the project before
direct file edits, rebases, or external KiCad changes.

## Diagnostics

1. Verify `codex mcp list` and the named server configuration.
2. Verify the server entrypoint, runtime dependencies, and `kicad-cli version`.
3. Check MCP UI/backend state and project-info tools.
4. Inspect server stderr and its documented log directory.
5. Run upstream TypeScript/Python tests after server changes.
6. Use GitNexus query/context/impact on the indexed server repository before
   implementation changes.

Keep installed paths in environment/configuration, not in this skill. See
`$kicad-toolchain-setup` for portable installation.

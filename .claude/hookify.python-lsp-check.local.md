---
name: python-lsp-check
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.pyi?$
---

**Python file modified — run LSP diagnostics.**

You MUST use the LSP tool to check for issues in this file:

1. Run `LSP` with `operation: "documentSymbol"` on the modified file to verify the server is active
2. Run `LSP` with `operation: "hover"` on any new or changed symbols to verify types are correct
3. If the LSP reports type errors or unresolved imports, **fix them immediately** before moving on

Do NOT skip this step. Every Python file edit must be validated by pyright.

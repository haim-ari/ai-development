---
name: check-env
description: Run full environment health check — packages, MPS GPU, API keys, Jupyter kernel, and venv status
---

Run a comprehensive environment health check and report results as a checklist.

## Instructions

Run the following checks in order using Bash:

1. **Python version and venv**: `which python && python --version`
   - Confirm path contains `.venv/bin/python`
   - Confirm version is `3.12.x`

2. **Package verification**: `python check_setup.py`
   - Report any missing packages

3. **MPS GPU availability**: `python -c "import torch; print('MPS available:', torch.backends.mps.is_available()); print('MPS built:', torch.backends.mps.is_built())"`
   - Both should be True on Apple Silicon

4. **API keys**: `test -f .env && echo '.env file exists' || echo '.env file MISSING — copy from .env.example'`
   - Do NOT read or print the contents of `.env`

5. **Jupyter kernel**: `jupyter kernelspec list 2>/dev/null | grep llm`
   - Should show the `llm` kernel

6. **Devbox status**: `devbox version`

Present results as a checklist with pass/fail status for each item. If anything fails, include the fix command from SETUP-MACOS.md.

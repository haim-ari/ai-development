# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **AI Developers Course** (March 2026) environment repo. It provides a fully isolated Python development environment on macOS Apple Silicon using **Devbox (Nix) + uv + direnv**. There is no application code here — the repo is an environment scaffold containing package definitions, setup tooling, and documentation for a multi-session course covering ML, NLP, LLMs, RAG, and agents.

## Environment Architecture

Three-layer isolation stack — nothing touches the host macOS:

1. **Devbox** (`devbox.json`) — Nix-based shell providing Python 3.12.13 and uv 0.10.9
2. **uv** — manages `.venv/` with 221 pinned packages from `requirements.txt`
3. **direnv** (`.envrc`) — auto-activates devbox + venv on `cd` into the project

The `init_hook` in `devbox.json` handles venv creation, activation, and first-run package installation (tracked by `.venv/.installed` sentinel).

## Commands

```bash
# Verify environment setup
python check_setup.py

# Run devbox test script (same as above)
devbox run test

# Launch Jupyter in browser
jupyter lab

# Add a package
uv pip install <package-name>
uv pip freeze > requirements.txt

# Recompile pinned requirements from source list
uv pip compile requirements.in -o requirements.txt

# Force reinstall all packages
rm .venv/.installed
uv pip install -r requirements.txt && touch .venv/.installed

# Re-register Jupyter kernel
python -m ipykernel install --user --name llm --display-name "Python (llm)"
```

## Key Files

- `devbox.json` — Nix package pins (Python, uv) and `init_hook` for auto-setup
- `requirements.in` — human-maintained direct dependencies, organized by course session
- `requirements.txt` — uv-compiled pinned lockfile (auto-generated, do not hand-edit)
- `.envrc` — single-line direnv config that delegates to devbox
- `check_setup.py` — imports all 21 required packages and reports status
- `.env.example` — template for API keys (OPENAI_API_KEY, CO_API_KEY, ANTHROPIC_API_KEY)
- `SETUP-MACOS.md` — full setup guide for students

## Package Groups (requirements.in)

| Sessions | Domain | Key Packages |
|----------|--------|-------------|
| 1-4 | Core | numpy, pandas, matplotlib, scikit-learn, jupyter |
| 2-7 | NLP & Deep Learning | torch (MPS), transformers, sentence-transformers, gensim, nltk |
| 5-8 | LLM & API | openai, cohere, anthropic, datasets |
| 9+ | RAG & Agents | chromadb, rank-bm25, langchain, langgraph |

## Important Conventions

- **API keys** go in `.env` (gitignored), loaded via `python-dotenv`. Never commit `.env`.
- **Package management** uses `uv`, not pip or conda. Always use `uv pip install` / `uv pip compile`.
- **Jupyter kernel** is named `"Python (llm)"` — used in both Cursor and browser JupyterLab.
- **PyTorch** is installed with MPS (Metal Performance Shaders) support for Apple Silicon GPU. Use `device="mps"` for GPU tensors.
- **Python version** is pinned to 3.12 (course requirement). Do not upgrade to 3.13+.

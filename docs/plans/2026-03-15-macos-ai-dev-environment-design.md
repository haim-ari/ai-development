# macOS AI Development Environment Setup — Design Document

**Date:** 2026-03-15
**Course:** AI Developers — March 2026 (AI Systems, RAG & Agents)
**Platform:** macOS 26.2, Apple Silicon (arm64)
**Strategy:** Devbox (Nix) + uv + direnv — zero changes to host macOS

---

## 1. Architecture

```
macOS (untouched)
  └── Devbox (Nix isolation layer)
       ├── Python 3.12.x (pinned via devbox.json)
       ├── uv (fast package manager)
       └── direnv (auto-activation)
            │
            ├── ai-developers/             ← base course repo
            │   ├── devbox.json            ← Nix packages (Python 3.12 + uv)
            │   ├── devbox.lock            ← pinned Nix hashes
            │   ├── .envrc                 ← direnv auto-activation
            │   ├── requirements.in        ← human-maintained package list
            │   ├── requirements.txt       ← uv-compiled pinned versions + hashes
            │   ├── .venv/                 ← uv-managed virtualenv
            │   ├── .env                   ← API keys (gitignored)
            │   └── check_setup.py         ← verification script
            │
            └── other-repos/               ← future course repos
                ├── devbox.json            ← copied from base
                ├── .envrc                 ← copied from base
                ├── requirements.in        ← base + per-repo extras
                ├── requirements.txt       ← compiled pins
                └── .venv/                 ← isolated venv
```

## 2. Nix Packages (devbox.json)

| Package  | Version  | Purpose                       |
|----------|----------|-------------------------------|
| python   | 3.12.x   | Course-specified Python        |
| uv       | latest   | Package management + venv      |

The `init_hook` in devbox.json will:
1. Create `.venv` via `uv venv --python 3.12` if missing
2. Activate `.venv/bin/activate`
3. Auto-install from `requirements.txt` if venv is fresh

## 3. Python Packages

### 3.1 Core (Sessions 1-4)
numpy, matplotlib, scikit-learn, pandas, jupyter, notebook, jupyterlab,
ipykernel, python-dotenv, requests, tqdm

### 3.2 NLP & Deep Learning (Sessions 2-7)
torch, torchvision, transformers, sentence-transformers, gensim, nltk, tiktoken

### 3.3 LLM & API (Sessions 5-8)
openai, cohere, anthropic, datasets, beautifulsoup4

### 3.4 RAG & Agents (Sessions 9+)
chromadb, rank-bm25, langchain, langchain-openai, langchain-community, langgraph

### 3.5 Jupyter Kernel
Registered as `"Python (llm)"` — visible in both VS Code and browser JupyterLab.

### 3.6 Pinning Strategy
- `requirements.in` — human-readable source list
- `uv pip compile` generates `requirements.txt` with exact versions + hashes
- All repos reference the same compiled output for reproducibility

## 4. VS Code Extensions

- ms-python.python
- ms-python.vscode-pylance
- ms-toolsai.jupyter
- ms-python.debugpy
- eamodio.gitlens

## 5. Daily Workflow

**Start a session:**
```bash
cd ~/vsCode/haim-ari/github/ai-developers
# direnv auto-activates devbox + .venv — ready instantly
```

**Jupyter in browser:**
```bash
jupyter lab
```

**Jupyter in VS Code:**
Open any `.ipynb`, select kernel "Python (llm)".

**New repo with same base:**
```bash
cd ~/vsCode/haim-ari/github/new-repo
cp ../ai-developers/devbox.json .
cp ../ai-developers/.envrc .
echo '-r ../ai-developers/requirements.txt' > requirements.in
echo 'some-extra-package' >> requirements.in
devbox shell
direnv allow
```

**Add a package:**
```bash
uv pip install new-package
uv pip freeze > requirements.txt
```

## 6. Decisions & Trade-offs

| Decision | Why | Alternative Rejected |
|----------|-----|---------------------|
| Devbox over direct install | Zero macOS pollution, reproducible | Homebrew Python — pollutes system |
| uv over conda | 10-100x faster, lighter, 2026 standard | Conda — heavy, slow, overkill |
| uv over pip | Speed, lockfile support, venv management | pip — slow, no compile/lock |
| direnv auto-activation | Seamless multi-terminal workflow | Manual `devbox shell` each time |
| Python 3.12 (not 3.14) | Course requirement, broader package compat | 3.14 — course specifies 3.12 |
| JupyterLab + VS Code | User needs both browser and editor workflows | One or the other |

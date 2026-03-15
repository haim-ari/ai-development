# macOS Setup Guide -- AI Developers Course

A complete, reproducible environment for the AI Developers course on macOS Apple Silicon. This guide uses **Devbox** (Nix-based isolation), **uv** (fast Python package manager), and **direnv** (automatic environment activation) to deliver a zero-pollution setup: nothing is installed into your system Python, Homebrew Python, or any global site-packages.

**Why not Conda?** Conda environments are slow to resolve, leak state into `~/.conda`, and often fight with macOS system libraries. Devbox gives you a hermetic Nix shell with pinned versions, uv resolves and installs hundreds of packages in seconds, and direnv makes it all invisible -- just `cd` into the repo and everything activates.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Quick Start (for this repo)](#3-quick-start-for-this-repo)
4. [What's Inside](#4-whats-inside)
5. [Using Jupyter](#5-using-jupyter)
6. [API Keys Setup](#6-api-keys-setup)
7. [Creating a New Repo with the Same Base](#7-creating-a-new-repo-with-the-same-base)
8. [Adding Packages](#8-adding-packages)
9. [Cursor Extensions](#9-cursor-extensions)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Overview

This environment consists of three layers:

| Layer | Tool | Purpose |
|-------|------|---------|
| Isolation | **Devbox 0.16.0** | Provides Python 3.12.13 and uv 0.10.9 via Nix, completely isolated from the host |
| Packages | **uv 0.10.9** | Installs 221 Python packages (including PyTorch with MPS) into a local `.venv` |
| Activation | **direnv 2.36.0** | Automatically enters the devbox shell and activates `.venv` when you `cd` into the project |

The result: you type `cd ai-developers` and everything is ready. Type `cd ..` and everything deactivates. No `source activate`, no `conda activate`, no manual steps.

---

## 2. Prerequisites

You need four things installed on your Mac before cloning this repo.

### 2.1 Homebrew

If you do not already have Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2.2 Devbox

Devbox manages the Nix-based isolated shell (Python, uv, and any future system tools):

```bash
curl -fsSL https://get.jetify.com/devbox | bash
```

Verify after installation:

```bash
devbox version
# Expected: 0.16.0 or later
```

### 2.3 direnv

direnv auto-activates the devbox environment when you enter the project directory:

```bash
brew install direnv
```

Then add the direnv hook to your shell. Open `~/.zshrc` in any editor and append:

```bash
# direnv -- auto-activate devbox environments on cd
eval "$(direnv hook zsh)"
```

Reload your shell:

```bash
source ~/.zshrc
```

### 2.4 Cursor IDE

Download and install Cursor from [https://cursor.sh](https://cursor.sh). Cursor is a VS Code fork with built-in AI features. All standard VS Code extensions work.

---

## 3. Quick Start (for this repo)

Once the prerequisites are installed, clone the repo and let direnv do the rest:

```bash
git clone <repo-url> ai-developers
cd ai-developers
direnv allow   # first time only -- grants direnv permission to run .envrc
```

That single `direnv allow` triggers the following chain automatically:

1. **direnv** reads `.envrc`, which calls `devbox generate direnv --print-envrc`.
2. **Devbox** enters its Nix shell, providing Python 3.12.13 and uv 0.10.9.
3. The **init_hook** in `devbox.json` creates `.venv` (if missing), activates it, and runs `uv pip install -r requirements.txt` (if packages are not yet installed).
4. You land in a fully configured shell with all 221 packages available.

On subsequent visits, just `cd ai-developers` -- direnv re-activates everything automatically with no delay.

**Verify the setup:**

```bash
python check_setup.py
```

This script imports every required package and reports its status. You should see all packages marked as installed, plus confirmation of your Python version and environment path.

---

## 4. What's Inside

### 4.1 Devbox Packages (devbox.json)

| Package | Pinned Version | Purpose |
|---------|---------------|---------|
| `python` | 3.12.13 | Course Python runtime |
| `uv` | 0.10.9 | Fast Python package installer and resolver |

### 4.2 The init_hook

The `devbox.json` file contains an `init_hook` that runs every time the devbox shell activates:

```json
"init_hook": [
  "export PATH=\"$HOME/.local/bin:$HOME/.npm-global/bin:/opt/homebrew/bin:$PATH\"",
  "if [ ! -d .venv ]; then uv venv --python python3.12 .venv; fi",
  ". .venv/bin/activate",
  "if [ -f requirements.txt ] && [ ! -f .venv/.installed ]; then uv pip install -r requirements.txt && touch .venv/.installed; fi"
]
```

What each line does:

1. **Restore host paths** -- re-adds `~/.local/bin`, `/opt/homebrew/bin` etc. to PATH so host tools like `claude`, `cursor`, `brew` remain available inside the devbox shell.
2. **Create .venv** -- only if it does not already exist. Uses uv to create a virtual environment pinned to Python 3.12.
3. **Activate .venv** -- sources the activate script so all `python` and `pip` commands use the local environment.
4. **Install packages** -- only on first run (tracked by `.venv/.installed` sentinel file). Installs all 221 packages from `requirements.txt` using uv.

### 4.3 Python Package Categories (requirements.in)

The `requirements.in` file defines the direct dependencies, organized by course section:

**Core (Sessions 1-4):**
`numpy`, `matplotlib`, `scikit-learn`, `pandas`, `jupyter`, `notebook`, `jupyterlab`, `ipykernel`, `python-dotenv`, `requests`, `tqdm`

**NLP and Deep Learning (Sessions 2-7):**
`torch`, `torchvision`, `transformers`, `sentence-transformers`, `gensim`, `nltk`, `tiktoken`

**LLM and API (Sessions 5-8):**
`openai`, `cohere`, `anthropic`, `datasets`, `beautifulsoup4`

**RAG and Agents (Sessions 9+):**
`chromadb`, `rank-bm25`, `langchain`, `langchain-openai`, `langchain-community`, `langgraph`

The `requirements.txt` file is the fully resolved (pinned) output with all 221 transitive dependencies.

---

## 5. Using Jupyter

The Jupyter kernel **"Python (llm)"** is pre-registered and available in both the browser and Cursor.

### 5.1 In the Browser

```bash
jupyter lab
```

Once JupyterLab opens in your browser, create a new notebook or open an existing `.ipynb` file. Select the **"Python (llm)"** kernel from the kernel picker in the top-right corner.

### 5.2 In Cursor

Open any `.ipynb` file in Cursor. Click the kernel selector in the top-right corner of the notebook editor and choose **"Python (llm)"** from the list.

### 5.3 Test GPU (Apple Silicon MPS)

PyTorch 2.10.0 is installed with MPS (Metal Performance Shaders) support for Apple Silicon GPU acceleration. Verify it works:

```python
import torch

print(f"PyTorch version: {torch.__version__}")        # 2.10.0
print(f"MPS available: {torch.backends.mps.is_available()}")  # True
print(f"MPS built: {torch.backends.mps.is_built()}")          # True

# Quick test: move a tensor to the GPU
x = torch.randn(3, 3, device="mps")
print(x)
```

If `mps.is_available()` returns `True`, your PyTorch installation can use the Apple Silicon GPU for training and inference.

---

## 6. API Keys Setup

Several course sessions require API keys for OpenAI, Cohere, and Anthropic.

1. Copy the example file:

```bash
cp .env.example .env
```

2. Open `.env` and fill in your actual keys:

```
OPENAI_API_KEY=sk-your-key-here
CO_API_KEY=your-cohere-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

3. The `.env` file is listed in `.gitignore` and will never be committed.

4. In your Python code, load the keys with:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env into os.environ

openai_key = os.getenv("OPENAI_API_KEY")
cohere_key = os.getenv("CO_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
```

---

## 7. Creating a New Repo with the Same Base

To set up a new project with the same toolchain:

```bash
mkdir my-new-project && cd my-new-project

# Copy the devbox and direnv configuration
cp /path/to/ai-developers/devbox.json .
cp /path/to/ai-developers/.envrc .

# Initialize devbox (downloads Nix packages if needed)
devbox install

# Allow direnv
direnv allow

# Create your own requirements
cp /path/to/ai-developers/requirements.in .

# Add any extra packages you need
echo "fastapi" >> requirements.in

# Compile and install
uv pip compile requirements.in -o requirements.txt
uv pip install -r requirements.txt

# Remove the sentinel so init_hook won't re-install on next entry
touch .venv/.installed
```

---

## 8. Adding Packages

To add a new package to the environment:

```bash
# Install the package into the active .venv
uv pip install package-name

# Update the pinned requirements file
uv pip freeze > requirements.txt
```

If you want to track the new package as a direct dependency, also add it to `requirements.in`:

```bash
echo "package-name" >> requirements.in
```

To re-install everything from scratch (e.g., after pulling new requirements):

```bash
rm .venv/.installed
# Exit and re-enter the directory, or run:
uv pip install -r requirements.txt && touch .venv/.installed
```

---

## 9. Cursor Extensions

The following extensions are installed for the AI Developers workflow:

| Extension | ID | Purpose |
|-----------|----|---------|
| Python | `ms-python.python` | Python language support, debugging, formatting |
| Pylance / cursorpyright | `ms-python.vscode-pylance` | Type checking, IntelliSense, auto-imports |
| Jupyter | `ms-toolsai.jupyter` | Notebook support inside Cursor |
| Debugpy | `ms-python.debugpy` | Python debugger |
| GitLens | `eamodio.gitlens` | Git blame, history, and annotations |

To install them from the command line:

```bash
cursor --install-extension ms-python.python
cursor --install-extension ms-python.vscode-pylance
cursor --install-extension ms-toolsai.jupyter
cursor --install-extension ms-python.debugpy
cursor --install-extension eamodio.gitlens
```

---

## 10. Troubleshooting

### "direnv not activating" when I cd into the project

1. Confirm the direnv hook is in your `~/.zshrc`:
   ```bash
   grep "direnv hook" ~/.zshrc
   ```
   If missing, add `eval "$(direnv hook zsh)"` and run `source ~/.zshrc`.

2. Grant permission for this directory:
   ```bash
   direnv allow
   ```

### "Python version wrong" or commands use system Python

Make sure you are inside the devbox environment:

```bash
which python
# Expected: /Users/<you>/vsCode/.../ai-developers/.venv/bin/python

python --version
# Expected: Python 3.12.13
```

If `which python` points to `/usr/bin/python3` or a Homebrew path, you are outside the devbox shell. Re-enter the directory or run `direnv allow`.

### "Package not found" / ModuleNotFoundError

The virtual environment may not have all packages installed:

```bash
# Confirm venv is active
echo $VIRTUAL_ENV
# Expected: /Users/<you>/vsCode/.../ai-developers/.venv

# Re-install all packages
uv pip install -r requirements.txt
```

### "Jupyter kernel not showing" in Cursor or JupyterLab

Re-register the kernel:

```bash
python -m ipykernel install --user --name llm --display-name "Python (llm)"
```

Then restart Cursor or refresh the JupyterLab browser tab.

### "torch MPS not available" -- mps.is_available() returns False

This typically means Python is running under Rosetta (x86 emulation) instead of native arm64:

```bash
python -c "import platform; print(platform.machine())"
# Expected: arm64
```

If it prints `x86_64`, your Python binary is not native. Ensure you are using the devbox-provided Python (which is arm64), not a Homebrew x86 installation or a Conda environment built for Intel.

Also confirm your macOS version supports MPS (macOS 12.3 or later):

```bash
sw_vers -productVersion
```

---

## Environment Summary

| Component | Version |
|-----------|---------|
| macOS | 26.2 (Apple Silicon arm64) |
| Devbox | 0.16.0 |
| Python | 3.12.13 |
| uv | 0.10.9 |
| direnv | 2.36.0 |
| PyTorch | 2.10.0 (MPS enabled) |
| IDE | Cursor |
| Installed packages | 221 |
| Jupyter kernel | "Python (llm)" |

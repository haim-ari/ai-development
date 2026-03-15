# macOS AI Dev Environment Setup — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Set up a fully isolated AI development environment on macOS using Devbox + uv + direnv, matching all course requirements without touching the host system.

**Architecture:** Devbox provides Python 3.12 + uv via Nix. uv manages a `.venv` with all course packages. direnv auto-activates everything on `cd`. Jupyter kernel registered for both Cursor and browser use.

**Tech Stack:** Devbox 0.16.0, Nix, uv 0.10.9, Python 3.12.13, direnv 2.36.0, Cursor IDE

---

### Task 1: Hook direnv into zsh

direnv is installed (`/opt/homebrew/bin/direnv`) but not hooked into the shell. Without this, auto-activation won't work.

**Files:**
- Modify: `~/.zshrc` (append one line)

**Step 1: Add the direnv hook**

```bash
echo '' >> ~/.zshrc
echo '# direnv — auto-activate devbox environments on cd' >> ~/.zshrc
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
```

**Step 2: Reload the shell**

```bash
source ~/.zshrc
```

**Step 3: Verify direnv hook is active**

```bash
direnv status
```

Expected: Output includes `Found RC allowed false` or similar — confirms hook is running.

---

### Task 2: Initialize devbox in the project

**Files:**
- Create: `ai-developers/devbox.json`
- Create: `ai-developers/devbox.lock` (auto-generated)

**Step 1: Initialize devbox**

```bash
cd /Users/haimari/vsCode/haim-ari/github/ai-developers
devbox init
```

**Step 2: Add Python 3.12 and uv**

```bash
devbox add python@3.12.13 uv@0.10.9
```

**Step 3: Verify packages are listed**

```bash
cat devbox.json
```

Expected: `"packages"` array contains `python@3.12.13` and `uv@0.10.9`.

**Step 4: Test the devbox shell**

```bash
devbox run -- python3 --version
```

Expected: `Python 3.12.13`

```bash
devbox run -- uv --version
```

Expected: `uv 0.10.9`

---

### Task 3: Configure devbox init_hook for auto-venv

**Files:**
- Modify: `ai-developers/devbox.json`

**Step 1: Update devbox.json with shell hooks**

Edit `devbox.json` to add the `shell` configuration:

```json
{
  "$schema": "https://raw.githubusercontent.com/jetify-com/devbox/main/.schema/devbox.schema.json",
  "packages": [
    "python@3.12.13",
    "uv@0.10.9"
  ],
  "shell": {
    "init_hook": [
      "if [ ! -d .venv ]; then uv venv --python python3.12 .venv; fi",
      ". .venv/bin/activate",
      "if [ -f requirements.txt ] && [ ! -f .venv/.installed ]; then uv pip install -r requirements.txt && touch .venv/.installed; fi"
    ]
  }
}
```

**Step 2: Test the hook**

```bash
devbox shell
```

Expected: `.venv` directory is created, shell prompt shows active venv.

**Step 3: Verify Python resolves to the venv**

Inside devbox shell:

```bash
which python
```

Expected: `/Users/haimari/vsCode/haim-ari/github/ai-developers/.venv/bin/python`

```bash
python --version
```

Expected: `Python 3.12.13`

Type `exit` to leave devbox shell.

---

### Task 4: Set up direnv auto-activation

**Files:**
- Create: `ai-developers/.envrc`

**Step 1: Generate the .envrc file**

```bash
cd /Users/haimari/vsCode/haim-ari/github/ai-developers
echo 'eval "$(devbox generate direnv --print-envrc)"' > .envrc
```

**Step 2: Allow direnv for this directory**

```bash
direnv allow
```

**Step 3: Verify auto-activation**

Leave and re-enter the directory:

```bash
cd ~ && cd /Users/haimari/vsCode/haim-ari/github/ai-developers
```

Expected: direnv loads automatically, `.venv` activates without manual `devbox shell`.

```bash
which python
```

Expected: Points to `.venv/bin/python`

---

### Task 5: Create requirements.in and compile requirements.txt

**Files:**
- Create: `ai-developers/requirements.in`
- Create: `ai-developers/requirements.txt` (compiled)

**Step 1: Create requirements.in with all course packages**

Write `requirements.in`:

```
# Core (Sessions 1-4)
numpy
matplotlib
scikit-learn
pandas
jupyter
notebook
jupyterlab
ipykernel
python-dotenv
requests
tqdm

# NLP & Deep Learning (Sessions 2-7)
torch
torchvision
transformers
sentence-transformers
gensim
nltk
tiktoken

# LLM & API (Sessions 5-8)
openai
cohere
anthropic
datasets
beautifulsoup4

# RAG & Agents (Sessions 9+)
chromadb
rank-bm25
langchain
langchain-openai
langchain-community
langgraph
```

**Step 2: Compile pinned requirements.txt**

Inside the devbox environment:

```bash
uv pip compile requirements.in -o requirements.txt
```

Expected: `requirements.txt` is generated with exact pinned versions for every package and transitive dependency.

**Step 3: Install all packages**

```bash
uv pip install -r requirements.txt
```

Expected: All packages install successfully. This may take 2-5 minutes (torch is large).

**Step 4: Mark venv as installed**

```bash
touch .venv/.installed
```

---

### Task 6: Register Jupyter kernel

**Files:**
- Kernel spec registered in user's Jupyter data directory

**Step 1: Register the kernel**

Inside devbox environment:

```bash
python -m ipykernel install --user --name llm --display-name "Python (llm)"
```

Expected: `Installed kernelspec llm in /Users/haimari/Library/Jupyter/kernels/llm`

**Step 2: Verify kernel is visible**

```bash
jupyter kernelspec list
```

Expected: Shows `llm` kernel pointing to the correct Python.

**Step 3: Test JupyterLab launch**

```bash
jupyter lab --no-browser &
```

Expected: Server starts, shows URL. Kill with `kill %1` after confirming.

---

### Task 7: Create verification script and .env template

**Files:**
- Create: `ai-developers/check_setup.py`
- Create: `ai-developers/.env.example`
- Create: `ai-developers/.gitignore`

**Step 1: Write check_setup.py**

```python
import sys

print(f"Python: {sys.version}")
print(f"Environment: {sys.prefix}")
print()

libs = {
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "sklearn": "scikit-learn",
    "torch": "torch",
    "transformers": "transformers",
    "sentence_transformers": "sentence-transformers",
    "gensim": "gensim",
    "nltk": "nltk",
    "openai": "openai",
    "tiktoken": "tiktoken",
    "dotenv": "python-dotenv",
    "chromadb": "chromadb",
    "langchain": "langchain",
    "cohere": "cohere",
    "anthropic": "anthropic",
    "bs4": "beautifulsoup4",
    "datasets": "datasets",
    "rank_bm25": "rank-bm25",
    "langgraph": "langgraph",
    "jupyterlab": "jupyterlab",
}

print("Package status:")
all_ok = True
for module, pkg in libs.items():
    try:
        __import__(module)
        print(f"  ✅ {pkg}")
    except ImportError:
        print(f"  ❌ {pkg} — run: uv pip install {pkg}")
        all_ok = False

print()
if all_ok:
    print("🎉 All packages installed correctly!")
else:
    print("⚠️  Some packages are missing. Install them and re-run.")
```

**Step 2: Write .env.example**

```
OPENAI_API_KEY=sk-your-key-here
CO_API_KEY=your-cohere-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Step 3: Write .gitignore**

```
.env
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.devbox/
```

**Step 4: Run the verification**

```bash
python check_setup.py
```

Expected: All packages show ✅.

---

### Task 8: Install Cursor extensions

**Files:** None (Cursor extensions are managed externally)

**Step 1: Install required extensions**

```bash
cursor --install-extension ms-python.python
cursor --install-extension ms-python.vscode-pylance
cursor --install-extension ms-toolsai.jupyter
cursor --install-extension ms-python.debugpy
cursor --install-extension eamodio.gitlens
```

**Step 2: Verify extensions**

```bash
cursor --list-extensions | grep -E "python|jupyter|debugpy|gitlens|pylance"
```

Expected: All 5 extensions listed.

---

### Task 9: Write the macOS setup guide (Markdown)

**Files:**
- Create: `ai-developers/SETUP-MACOS.md`

Write a clean, step-by-step Markdown guide that documents the entire setup process as executed. This becomes the reference doc for reproducing the environment or onboarding to new repos.

The guide should cover:
1. Prerequisites (Homebrew, Devbox, direnv)
2. direnv shell hook
3. Cloning and entering the repo
4. Devbox auto-setup (what happens automatically)
5. Verifying the environment
6. Using Jupyter (browser + Cursor)
7. Setting up API keys
8. Creating a new repo with the same base
9. Troubleshooting common issues

---

### Task 10: Final end-to-end verification

**Step 1: Leave and re-enter the directory**

```bash
cd ~ && cd /Users/haimari/vsCode/haim-ari/github/ai-developers
```

Expected: direnv auto-activates, no manual steps needed.

**Step 2: Run check_setup.py**

```bash
python check_setup.py
```

Expected: All ✅, Python 3.12.13, environment points to `.venv`.

**Step 3: Open a Jupyter notebook**

```bash
jupyter lab
```

Expected: JupyterLab opens in browser, "Python (llm)" kernel available.

**Step 4: Test in Cursor**

Open the project in Cursor, create a new `.ipynb` file, select "Python (llm)" kernel, run:

```python
import torch
print(torch.backends.mps.is_available())  # Should print True on Apple Silicon
```

Expected: `True`

**Step 5: Verify nothing was installed on host macOS**

```bash
/usr/bin/python3 --version
```

Expected: Shows the system Python (not 3.12.13) — confirms devbox isolation.

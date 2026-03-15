---
name: new-notebook
description: Create a new Jupyter notebook for a specific course session with standard imports, API key loading, and MPS device setup
---

Create a Jupyter notebook (.ipynb) for a course session.

## Usage

`/new-notebook <session-number> <topic>`

Example: `/new-notebook 3 "Linear Regression with scikit-learn"`

## Instructions

1. Ask for the session number and topic if not provided as arguments.

2. Based on the session number, include the appropriate imports in the first code cell. Sessions may span multiple groups — include all that apply:

   | Sessions | Group | Packages |
   |----------|-------|----------|
   | 1-4 | Core | numpy, pandas, matplotlib, scikit-learn |
   | 2-7 | NLP & Deep Learning | torch, transformers, sentence-transformers, gensim, nltk, tiktoken |
   | 5-8 | LLM & API | openai, cohere, anthropic, datasets, beautifulsoup4 |
   | 9+ | RAG & Agents | chromadb, rank_bm25, langchain, langchain_openai, langchain_community, langgraph |

3. The first code cell MUST always include:
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()
   ```

4. For sessions 5+, add API key loading after `load_dotenv()`:
   ```python
   openai_key = os.getenv("OPENAI_API_KEY")
   # Add cohere/anthropic keys as relevant to the session topic
   ```

5. For sessions 2-7 (torch sessions), add a second code cell for MPS device setup:
   ```python
   import torch

   device = "mps" if torch.backends.mps.is_available() else "cpu"
   print(f"Using device: {device}")
   ```

6. Add a markdown cell with the session title as `# Session <N>: <Topic>`.

7. Create the notebook file at the project root as `session_<N>_<slug>.ipynb` where `<slug>` is the topic in lowercase with underscores.

8. Use the NotebookEdit tool to create the notebook. Set the kernel to `llm` (display name "Python (llm)").

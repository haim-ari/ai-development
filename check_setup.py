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

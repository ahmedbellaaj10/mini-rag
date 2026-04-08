# mini-rag

A minimal Retrieval-Augmented Generation (RAG) pipeline built in Python.

> This project is a lightweight implementation of a RAG system, designed to retrieve relevant context from a document store and augment language model responses with that context.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ahmedbellaaj10/mini-rag.git
cd mini-rag
```

### 2. Install `uv` (if you don't have it)

[`uv`](https://docs.astral.sh/uv/) is a fast Python package and project manager. Install it with:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or via pip:

```bash
pip install uv
```

### 3. Set up the project environment

```bash
uv sync --all-groups
```

This will create a virtual environment and install all dependencies (including dev tools) using the pinned versions from `uv.lock`.

---

## Tooling

This project uses a modern Python toolchain to ensure code quality and consistent commits.

### [`uv`](https://docs.astral.sh/uv/)

A fast, all-in-one Python package manager and project manager (replaces `pip`, `pip-tools`, `virtualenv`, and more). It manages the virtual environment, dependencies, and Python version (pinned to `3.13` via `.python-version`).

### [`pre-commit`](https://pre-commit.com/)

A framework for managing and running git hooks before commits are made. Hooks run automatically on `git commit` to catch issues early. To install the hooks locally:

```bash
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

The following hooks are configured:

| Hook | Purpose |
|------|---------|
| `trailing-whitespace` | Removes trailing whitespace |
| `end-of-file-fixer` | Ensures files end with a newline |
| `check-yaml` | Validates YAML files |
| `check-toml` | Validates TOML files |
| `check-json` | Validates JSON files |
| `check-added-large-files` | Prevents large files from being committed |
| `check-merge-conflict` | Detects leftover merge conflict markers |
| `mixed-line-ending` | Enforces consistent line endings |
| `commitizen` | Validates commit message format |
| `ruff` | Lints and formats Python code |

### [`commitizen`](https://commitizen-tools.github.io/commitizen/)

Enforces [Conventional Commits](https://www.conventionalcommits.org/) message format (e.g., `feat:`, `fix:`, `chore:`). Beyond commit validation, it also handles versioning and changelog generation — automatically bumping the version, tagging the release, and updating `CHANGELOG.md` based on commit history.

Run it interactively to create a valid commit message:

```bash
uv run cz commit
```

Bump the version and generate a changelog:

```bash
uv run cz bump
```

### [`ruff`](https://docs.astral.sh/ruff/)

An extremely fast Python linter and formatter (replaces `flake8`, `isort`, `black`, and more). It runs automatically via pre-commit, but you can also run it manually:

```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .
```

---

## License

[Apache License 2.0](LICENSE)

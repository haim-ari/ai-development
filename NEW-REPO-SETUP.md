# Setting Up a New Course Repository

## Setup (2 commands)

```bash
mkdir my-new-repo && cd my-new-repo
../ai-developers/init-repo.sh
direnv allow
```

That's it. Devbox creates the venv, installs all 221 base packages, and activates everything automatically.

## Adding packages

Add package names to `requirements.in`, then:

```bash
uv pip install -r requirements.in
```

## Overriding a base package version

Edit the version directly in `requirements.in` (e.g., change `numpy` to `numpy==2.3.0`), then reinstall:

```bash
rm .venv/.installed && uv pip install -r requirements.in && touch .venv/.installed
```

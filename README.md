# envkeep

Personal CLI tool for managing encrypted .env files in my Python projects.

## What it does

- Encrypts .env files so I can commit them safely to git
- Decrypts them when I clone projects later
- Keeps backups with timestamps

## Installation

In your project's virtual environment:
```bash
# with uv
uv pip install git+https://github.com/EmmanuelNiyonshuti/envkeep.git

# with pip
pip install git+https://github.com/EmmanuelNiyonshuti/envkeep.git
```

## Usage
```bash
# First time in a project
envkeep init                    # creates .envkeep/ folder and encryption key
envkeep encrypt                 # creates .env.encrypted from .env
git add .env.encrypted .envkeep/
git commit -m "add encrypted env"

# Make sure .env and .env.key are in .gitignore

# When cloning later
git clone <your-repo>
cd <your-repo>
export ENVKEEP_KEY=<your-saved-key>  # get this from where you saved your key
envkeep decrypt                       # recreates .env

# Other commands
envkeep backup                  # backup current .env.encrypted
envkeep restore --backup <timestamp>
envkeep status                  # show project info
```

## Important

- After `envkeep init`, save the key from `.env.key` somewhere safe (e.g: password manager)
- The key is needed to decrypt on other machines
- Never commit `.env` or `.env.key` to git

## Example .gitignore
```
.env
.env.key
```

## Requirements

- Python 3.8+
- Virtual environment (recommended)
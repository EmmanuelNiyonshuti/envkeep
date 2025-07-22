# EnvKeep CLI

A secure, local CLI tool to manage your project's `.env` files with encryption, backup, and restore features.

## Features
- Initialize project for secure .env management
- Encrypt and decrypt .env files using a symmetric key
- Backup and restore encrypted .env files
- Project status overview

## Installation

### With pip
```bash
pip install .
```

### With Poetry
```bash
poetry install
```

## Usage

```bash
envkeep init
envkeep encrypt [--file .env]
envkeep decrypt [--file .env.encrypted]
envkeep backup
envkeep restore [--backup TIMESTAMP]
envkeep status
```

See `envkeep --help` for all options.

## Requirements
- Python 3.11+
- [cryptography](https://pypi.org/project/cryptography/)
- [typer](https://pypi.org/project/typer/)

## Example .env
```
SECRET_KEY=supersecret
DATABASE_URL=sqlite:///db.sqlite3
DEBUG=True
```

## Security
- The encryption key is never stored in the repository.
- You must set the `ENVKEEP_KEY` environment variable or save the generated key securely.

## License
MIT
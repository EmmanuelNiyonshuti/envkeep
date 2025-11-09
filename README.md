# envkeep CLI

A simple CLI tool I use to manage encrypted .env files in Python projects.
Still evolving, but currently supports:

Project initialization for secure .env management

Encrypting and decrypting .env files with symmetric encryption

Backing up and restoring encrypted .env files

Viewing project status


Built with Typer and Cryptography
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


## Security
- The encryption key is never stored in the repository.
- You must set the `ENVKEEP_KEY` environment variable
## License
MIT

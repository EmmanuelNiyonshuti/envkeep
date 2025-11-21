import os
from datetime import datetime
from pathlib import Path
import typer
from . import config, core, utils

app = typer.Typer(help="EnvKeep: Securely manage your .env files per project.")

@app.command()
def init():
    """Initialize the current project for envkeep usage."""
    if config.ENVKEEP_DIR.exists():
        typer.secho("Project already initialized for EnvKeep.", fg=typer.colors.YELLOW)
        return
    config.ENVKEEP_DIR.mkdir(parents=True, exist_ok=True)
    project_name = Path.cwd().name
    created_at = datetime.now().isoformat()
    meta = {
        config.CONFIG_KEYS["project_name"]: project_name,
        config.CONFIG_KEYS["created_at"]: created_at,
        config.CONFIG_KEYS["backups"]: [],
        config.CONFIG_KEYS["last_backup"]: None,
    }
    utils.write_json(config.CONFIG_FILE, meta)
    utils.ensure_gitignore()
    if Path(".env.key").exists() or os.environ.get(config.ENVKEEP_KEY_ENV):
        typer.secho(
            "ENVKEEP_KEY found in environment or .env.key file.", fg=typer.colors.GREEN
        )
        return
    new_key = core.generate_key()
    with open(".env.key", "w") as f:
        f.write(f"ENVKEEP_KEY={new_key}\n")
    utils.ensure_gitignore(".env.key")
    typer.secho(
        "No ENVKEEP_KEY found. A new key has been generated and written to .env.key.",
        fg=typer.colors.BLUE,
    )
    typer.secho(
        "Keep .env.key secret! It is required to decrypt your encrypted .env file.",
        fg=typer.colors.YELLOW,
        bold=True,
    )
    typer.secho(
        ".env.key has been added to .gitignore automatically.", fg=typer.colors.BLUE
    )
    typer.secho(
        "You can also set ENVKEEP_KEY in your shell if you prefer:",
        fg=typer.colors.BLUE,
    )
    typer.secho(f"export ENVKEEP_KEY={new_key}", fg=typer.colors.GREEN)


@app.command()
def encrypt(
    file: Path = typer.Option(
        config.DEFAULT_ENV_FILE, "--file", help=".env file to encrypt"
    ),
):
    """Encrypt the specified .env file."""
    try:
        key = core.get_key()
    except:
        raise typer.Exit(code=1)
    if not file.exists():
        typer.secho(f"Ooops! File: {file} does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    output = file.parent / (
        file.name + ".encrypted" if not file.name.endswith(".encrypted") else file.name
    )
    if output.exists() and not utils.prompt_overwrite(output):
        raise typer.Exit(code=1)
    if core.encrypt_file(file, output, key):
        typer.secho(f"Encrypted {file} written to {output}", fg=typer.colors.GREEN)


@app.command()
def decrypt(
    file: Path = typer.Option(
        config.DEFAULT_ENCRYPTED_FILE, "--file", help="Encrypted file to decrypt"
    ),
):
    """Decrypt the specified encrypted file."""
    try:
        key = core.get_key()
        if not file.exists():
            typer.secho(f"File {file} does not exist.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        output = file.parent / (
            file.name.replace(".encrypted", "")
            if file.name.endswith(".encrypted")
            else ".env"
        )
        if output.exists() and not utils.prompt_overwrite(output):
            raise typer.Exit(code=1)
        if core.decrypt_file(file, output, key):
            typer.secho(
                f"Decrypted {file} and written to {output}", fg=typer.colors.GREEN
            )
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)


@app.command()
def backup():
    """Backup the current .env.encrypted file."""
    src = config.DEFAULT_ENCRYPTED_FILE
    if not src.exists():
        typer.secho(f"No {src} file to backup.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    config.BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = config.BACKUPS_DIR / f".env.encrypted.{timestamp}"
    if utils.safe_copy(src, backup_file, overwrite=False):
        meta = utils.read_json(config.CONFIG_FILE) or {}
        backups = meta.get(config.CONFIG_KEYS["backups"], [])
        backups.append(timestamp)
        meta[config.CONFIG_KEYS["backups"]] = backups
        meta[config.CONFIG_KEYS["last_backup"]] = timestamp
        utils.write_json(config.CONFIG_FILE, meta)
        typer.secho(f"Backup created: {backup_file}", fg=typer.colors.GREEN)


@app.command()
def restore(
    backup: str | None = typer.Option(
        None, "--backup", help="Timestamp of backup to restore"
    ),
):
    """Restore a backup to .env.encrypted. Lists available backups if no timestamp is given."""
    meta = utils.read_json(config.CONFIG_FILE) or {}
    backups = meta.get(config.CONFIG_KEYS["backups"], [])
    if not backups:
        typer.secho("No backups found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if not backup:
        typer.secho("Available backups:", fg=typer.colors.BLUE)
        for ts in backups:
            typer.echo(ts)
        return
    backup_file = config.BACKUPS_DIR / f".env.encrypted.{backup}"
    if not backup_file.exists():
        typer.secho(f"Backup {backup} not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    if utils.safe_copy(backup_file, config.DEFAULT_ENCRYPTED_FILE, overwrite=True):
        typer.secho(
            f"Restored backup {backup} to {config.DEFAULT_ENCRYPTED_FILE}",
            fg=typer.colors.GREEN,
        )


@app.command()
def status():
    """Show current project status and recent backups."""
    initialized = config.ENVKEEP_DIR.exists() and config.CONFIG_FILE.exists()
    typer.secho(
        f"Project initialized: {'Yes' if initialized else 'No'}",
        fg=typer.colors.GREEN if initialized else typer.colors.RED,
    )
    if initialized:
        meta = utils.read_json(config.CONFIG_FILE) or {}
        typer.secho(
            f"Project: {meta.get(config.CONFIG_KEYS['project_name'], '-')}",
            fg=typer.colors.BLUE,
        )
        typer.secho(
            f"Created: {meta.get(config.CONFIG_KEYS['created_at'], '-')}",
            fg=typer.colors.BLUE,
        )
        typer.secho(
            f"Last backup: {meta.get(config.CONFIG_KEYS['last_backup'], '-')}",
            fg=typer.colors.BLUE,
        )
        backups = meta.get(config.CONFIG_KEYS["backups"], [])
        if backups:
            typer.secho("Recent backups:", fg=typer.colors.BLUE)
            for ts in backups[-5:]:
                typer.echo(f"- {ts}")
        else:
            typer.secho("No backups found.", fg=typer.colors.YELLOW)
    try:
        key = core.get_key()
        typer.secho(
            f"Key status: {'Set' if key else 'Not set'}",
            fg=typer.colors.GREEN if key else typer.colors.RED,
        )
    except Exception as e:
        typer.secho(f"Key is not set: {e}", fg=typer.colors.RED)



@app.command()
def push():
    """ push encrypted file"""
@app.command()
def pull():
    """ pull encrypted file"""


if __name__ == "__main__":
    app()

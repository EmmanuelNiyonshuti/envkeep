import json
from pathlib import Path
from typing import Any
import typer


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        typer.secho(f"Error reading {path}: {e}", fg=typer.colors.RED)
        return None


def write_json(path: Path, data: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        typer.secho(f"Error writing {path}: {e}", fg=typer.colors.RED)


def safe_copy(src: Path, dst: Path, overwrite: bool = False) -> bool:
    if dst.exists() and not overwrite:
        typer.secho(
            f"File {dst} already exists. Not overwriting.", fg=typer.colors.YELLOW
        )
        return False
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
            fdst.write(fsrc.read())
        return True
    except Exception as e:
        typer.secho(f"Error copying {src} to {dst}: {e}", fg=typer.colors.RED)
        return False


def prompt_overwrite(path: Path) -> bool:
    if not path.exists():
        return True
    return typer.confirm(f"{path} already exists. Overwrite?", abort=True)


def file_exists(path: Path) -> bool:
    return path.exists()


def ensure_gitignore(filename: str = ".envkeep"):
    gitignore = Path(".gitignore")
    if not gitignore.exists():
        with open(gitignore, "w") as f:
            f.write(f"{filename}/\n")
        return
    with open(gitignore, "r+") as f:
        lines = f.readlines()
        if f"{filename}/" not in [l.strip() for l in lines]:
            f.write(f"\n{filename}/\n")

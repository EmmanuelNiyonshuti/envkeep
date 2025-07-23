import os
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
import typer
from dotenv import load_dotenv
import re

from .config import ENVKEEP_KEY_ENV, FERNET_KEY_LENGTH, FERNET_KEY_PATTERN


def get_key() -> Optional[bytes]:
    key = os.environ.get(ENVKEEP_KEY_ENV)
    if not key:
        key_path = Path(".env.key")
        if not (key_path.exists() and key_path.is_file()):
            raise FileNotFoundError(
                ".env.key file is missing or unreadable, and ENVKEEP_KEY is not set."
            )
        load_dotenv(dotenv_path=key_path)
        key = os.environ.get(ENVKEEP_KEY_ENV)
    key = (key or "").strip()
    if len(key) != FERNET_KEY_LENGTH and re.fullmatch(FERNET_KEY_PATTERN, key) is None:
        raise ValueError(
            "Invalid key - expected 44 characters (base64-encoded Fernet key)"
        )
    try:
        Fernet(key.encode())
    except Exception as e:
        raise ValueError("Invalid Fernet key format.") from e
    return key.encode()


def generate_key() -> str:
    return Fernet.generate_key().decode()


def encrypt_file(input_path: Path, output_path: Path, key: bytes) -> bool:
    try:
        with open(input_path, "rb") as f:
            data = f.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        with open(output_path, "wb") as f:
            f.write(encrypted)
        return True
    except Exception as e:
        typer.secho(f"Encryption failed: {e}", fg=typer.colors.RED)
        return False


def decrypt_file(input_path: Path, output_path: Path, key: bytes) -> bool:
    try:
        # read from the .env.encrypted file
        with open(input_path, "rb") as f:
            data = f.read()
        if not data:
            typer.secho("Invalid data, nothing to decrypt.", fg=typer.colors.YELLOW)
            return False
        fernet = Fernet(key)
        # decrypt the data and write to .env file
        decrypted = fernet.decrypt(data)
        with open(output_path, "wb") as f:
            f.write(decrypted)
        return True
    except InvalidToken:
        typer.secho(
            "Decryption failed: Invalid key or corrupted file.", fg=typer.colors.RED
        )
        return False
    except Exception as e:
        typer.secho(f"Decryption failed: {e}", fg=typer.colors.RED)
        return False

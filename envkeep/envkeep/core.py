import os
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
import typer
from dotenv import load_dotenv
from .config import ENVKEEP_KEY_ENV, FERNET_KEY_LENGTH


def get_key() -> Optional[bytes]:
    # Try environment variable first
    key = os.environ.get(ENVKEEP_KEY_ENV)
    if not key:
        # Try loading from .env.key file
        if Path('.env.key').exists():
            load_dotenv('.env.key')
            key = os.environ.get(ENVKEEP_KEY_ENV)
    if key:
        if len(key) == FERNET_KEY_LENGTH:
            try:
                # Validate base64
                Fernet(key.encode())
                return key.encode()
            except Exception:
                typer.secho("ENVKEEP_KEY is invalid. Must be a valid Fernet key.", fg=typer.colors.RED)
                return None
        else:
            typer.secho(f"ENVKEEP_KEY must be {FERNET_KEY_LENGTH} characters (base64)", fg=typer.colors.RED)
            return None
    return None

def generate_key() -> str:
    return Fernet.generate_key().decode()

def encrypt_file(input_path: Path, output_path: Path, key: bytes) -> bool:
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        with open(output_path, 'wb') as f:
            f.write(encrypted)
        return True
    except Exception as e:
        typer.secho(f"Encryption failed: {e}", fg=typer.colors.RED)
        return False

def decrypt_file(input_path: Path, output_path: Path, key: bytes) -> bool:
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)
        with open(output_path, 'wb') as f:
            f.write(decrypted)
        return True
    except InvalidToken:
        typer.secho("Decryption failed: Invalid key or corrupted file.", fg=typer.colors.RED)
        return False
    except Exception as e:
        typer.secho(f"Decryption failed: {e}", fg=typer.colors.RED)
        return False 
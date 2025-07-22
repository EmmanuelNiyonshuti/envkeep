import os
from pathlib import Path

# Constants
ENVKEEP_DIR = Path('.envkeep')
CONFIG_FILE = ENVKEEP_DIR / 'config.json'
BACKUPS_DIR = ENVKEEP_DIR / 'backups'
DEFAULT_ENV_FILE = Path('.env')
DEFAULT_ENCRYPTED_FILE = Path('.env.encrypted')

# Key management
ENVKEEP_KEY_ENV = 'ENVKEEP_KEY'
FERNET_KEY_LENGTH = 44  # Fernet key is 32 bytes, base64 encoded

# Project metadata keys
CONFIG_KEYS = {
    'project_name': 'project_name',
    'created_at': 'created_at',
    'last_backup': 'last_backup',
    'backups': 'backups',
}
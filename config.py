import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)



os.makedirs(BASE_DIR / "instance", exist_ok=True)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "altere-esta-chave-em-producao")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{(BASE_DIR / 'instance' / 'estoque.db').resolve()}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False, "timeout": 30},
        "pool_pre_ping": True,
    }
    ITEMS_PER_PAGE = int(os.getenv("ITEMS_PER_PAGE", 10))
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    DEFAULT_ADMIN_USERNAME = os.getenv("ADMIN_USER", "admin")
    DEFAULT_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    DEFAULT_ADMIN_FULL_NAME = os.getenv("ADMIN_FULL_NAME", "Administrador")

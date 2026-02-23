from __future__ import annotations

from pathlib import Path
import sys


def project_root() -> Path:
    """Resolve project root for source and PyInstaller builds."""
    if getattr(sys, "frozen", False):
        # Use executable directory in frozen apps so data/logs remain writable.
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def client_root() -> Path:
    return project_root() / "client"


def data_dir() -> Path:
    path = client_root() / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


def db_path() -> Path:
    return data_dir() / "local.db"

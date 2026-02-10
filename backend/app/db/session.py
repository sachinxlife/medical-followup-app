"""Backward-compatible re-export for legacy imports.

Prefer using app.database.session and app.database.deps directly.
"""

from app.database.deps import get_db
from app.database.session import AsyncSessionLocal, engine

__all__ = ["engine", "AsyncSessionLocal", "get_db"]

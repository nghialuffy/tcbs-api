"""The JWT token response returned by ``get_token``."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TokenResponseDto:
    token: str | None = None

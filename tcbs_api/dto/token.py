"""The JWT token response returned by ``get_token``."""

from __future__ import annotations

from pydantic import Field

from tcbs_api.dto.base import DtoModel


class TokenResponseDto(DtoModel):
    token: str | None = Field(default=None, description="JWT token for subsequent requests.")

"""Exchange an API key for the JWT token that every other call needs."""

from __future__ import annotations

from tcbs_api.dto.auth.token_response_dto import TokenResponseDto
from tcbs_api.utils import request_api


def get_token(api_key: str, otp: str) -> TokenResponseDto:
    """Exchange an API key and OTP for a JWT access token.

    Operation 1.1 — https://developers.tcbs.com.vn/docs/v1.0.0/auth/token/

    This is the only unauthenticated endpoint. TCBS rate limits it to 10 requests per
    day, so cache the returned token instead of calling this for every request.
    """
    payload = request_api.post("/gaia/v1/oauth2/openapi/token", body={"apiKey": api_key, "otp": otp})
    return request_api.decode(TokenResponseDto, payload)

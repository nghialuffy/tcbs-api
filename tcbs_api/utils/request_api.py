"""Shared request plumbing for every TCBS Open API call.

Every public function in :mod:`tcbs_api.service` funnels through this module, so the parts
that are identical across all 28 endpoints — the production base URL, the bearer headers,
the HTTP verb, the status check, and the ``dacite`` decoding of the response — are written
once instead of being repeated in each function.

The derivative endpoints are the one variation: they wrap their payload in a
``{cmd, rc, rs, oID, data}`` envelope and are decoded with ``dataclasses_json`` rather than
``dacite``. That handling lives with them, in
:mod:`tcbs_api.service.derivative.derivative`.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, TypeVar

import requests
from dacite import Config, from_dict

from tcbs_api.utils import constant

__all__ = ["decode", "get", "get_headers", "post", "put"]

T = TypeVar("T")

# The token endpoint is the only call that is not authenticated.
_JSON_HEADERS: dict[str, str] = {"Content-Type": "application/json"}

# TCBS omits optional fields and returns fields this library does not model, so decoding
# cannot be strict.
_LENIENT = Config(strict=False)


def get_headers(token: str) -> dict[str, str]:
    """Build the JSON and bearer-token headers used by every authenticated call."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _headers(token: str | None) -> dict[str, str]:
    """Bearer headers, or JSON-only headers for the unauthenticated token endpoint."""
    return get_headers(token) if token is not None else dict(_JSON_HEADERS)


def _call(send: Callable[..., requests.Response], path: str, token: str | None, **kwargs: Any) -> Any:
    """Send one request to `path` and return its JSON body.

    Raises ``requests.HTTPError`` if the response status is not 2xx.
    """
    url = f"{constant.BASE_URL_PRODUCTION}{path}"
    response = send(url, headers=_headers(token), **kwargs)
    response.raise_for_status()
    return response.json()


def get(path: str, token: str | None = None, *, params: Mapping[str, Any] | None = None) -> Any:
    """``GET`` `path`, sending `params` as the query string."""
    return _call(requests.get, path, token, params=params)


def post(path: str, token: str | None = None, *, body: Any = None) -> Any:
    """``POST`` `body` as JSON to `path`."""
    return _call(requests.post, path, token, json=body)


def put(path: str, token: str | None = None, *, body: Any = None) -> Any:
    """``PUT`` `body` as JSON to `path`."""
    return _call(requests.put, path, token, json=body)


def decode(data_class: type[T], payload: Any) -> T:
    """Map a bare JSON object onto `data_class`, leniently.

    Unknown fields are ignored and missing fields fall back to their defaults, because
    TCBS does not always return every field the DTOs declare.
    """
    return from_dict(data_class=data_class, data=payload, config=_LENIENT)

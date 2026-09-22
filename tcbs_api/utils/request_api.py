"""Shared request plumbing for every TCBS Open API call.

Every public function in `tcbs_api.service` funnels through this module, so the parts
that are identical across all 19 endpoints — the production base URL, the bearer headers,
the HTTP verb, the status check, and the decoding of the response onto a pydantic model — are
written once instead of being repeated in each function.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, TypeVar

import requests
from pydantic import BaseModel

from tcbs_api.utils import constant

__all__ = ["decode", "get", "post"]

T = TypeVar("T", bound=BaseModel)


def _headers(token: str | None) -> dict[str, str]:
    """Bearer headers, or JSON-only headers for the unauthenticated token endpoint."""
    if token is None:
        return {"Content-Type": "application/json"}
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


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


def decode(model: type[T], payload: Any) -> T:
    """Validate a bare JSON payload into `model`.

    Pydantic does the work: it coerces in lax mode, ignores keys the model does not declare and
    fills declared fields the payload omits from their defaults. A payload that still does not
    fit — a required field missing, a value it cannot coerce — raises ``ValidationError``, whose
    ``errors()`` say which field and what arrived.

    A JSON key that is not a legal Python name — ``as`` in the 5.5 rows — is declared on the
    field as ``Field(alias="as")``.
    """
    return model.model_validate(payload)

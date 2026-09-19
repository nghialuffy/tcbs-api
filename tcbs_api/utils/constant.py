"""Production endpoint for the TCBS Open API.

TCBS publishes a single host — there is no sandbox or test host — so despite the name
there is nothing for callers to switch to.
"""

from __future__ import annotations

BASE_URL_PRODUCTION: str = "https://openapi.tcbs.com.vn"

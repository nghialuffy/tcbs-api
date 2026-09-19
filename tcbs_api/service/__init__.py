"""One module per API domain; each function is a thin declaration of one endpoint.

Every function takes the JWT ``token`` as its final positional argument and returns a
decoded DTO. The HTTP work — base URL, headers, verb, status check, JSON parsing — is not
repeated in these modules: it all goes through :mod:`tcbs_api.utils.request_api`.

* :mod:`tcbs_api.service.auth` — exchange an API key for a token
* :mod:`tcbs_api.service.account` — sub-account profile
* :mod:`tcbs_api.service.stock` — stock orders, trades, purchasing power, assets, cash
* :mod:`tcbs_api.service.market` — cash-market price board, foreign room, supply and demand
"""

from __future__ import annotations

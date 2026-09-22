"""One module per API domain; each function is a thin declaration of one endpoint.

Every function takes the JWT ``token`` as its final positional argument and returns a
decoded DTO. The HTTP work — base URL, headers, verb, status check, JSON parsing — is not
repeated in these modules: it all goes through `tcbs_api.utils.request_api`.

* `tcbs_api.service.token` — exchange an API key for a token
* `tcbs_api.service.account` — sub-account profile
* `tcbs_api.service.stock` — stock orders, trades, purchasing power, assets, cash
* `tcbs_api.service.market` — cash-market price board, foreign room, supply and demand
"""

from __future__ import annotations

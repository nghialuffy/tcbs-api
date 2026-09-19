"""Request and response models, grouped by API domain.

Every model is a plain ``dataclass`` whose field names match the JSON keys TCBS sends and
expects, keeping their original camelCase — ``OrderInfo.orderID`` and
``TotalCashDerivativeResponse.cashavaiwithdraw`` are spelled the way the API spells them
rather than the way Python normally would. That keeps the mapping between code and API
payloads obvious, and is why responses can be decoded straight onto these classes.

Sub-packages:

* :mod:`tcbs_api.dto.account` — profile information for a sub-account
* :mod:`tcbs_api.dto.auth` — the JWT token response
* :mod:`tcbs_api.dto.money` — cash transfers, margin deposit and withdrawal
* :mod:`tcbs_api.dto.stock_normal` — stock orders, purchasing power, assets and cash
* :mod:`tcbs_api.dto.market` — cash-market price board, foreign room, supply and demand
* :mod:`tcbs_api.dto.derivative_dto` — derivatives cash, positions, orders and market data
"""

from __future__ import annotations

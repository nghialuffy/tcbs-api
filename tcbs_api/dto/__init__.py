"""Request and response models, grouped by API domain.

Every model is a plain ``dataclass`` whose field names match the JSON keys TCBS sends and
expects, keeping their original camelCase — ``OrderDetail.orderID`` and
``CashInvestmentInfo.pp0forBF`` are spelled the way the API spells them rather than the way
Python normally would. That keeps the mapping between code and API payloads obvious, and is
why responses can be decoded straight onto these classes.

Each model carries exactly the fields TCBS's OpenAPI document declares for its operation —
nothing inferred, nothing extra — so what a DTO exposes is what the API documents. Two
consequences apply to every module below, so they are stated once here:

* A field the document declares ``int64`` is an ``int``; one declared ``number``/``double``
  is a ``float``, because ``dacite`` accepts an integer for a ``float`` field but not a float
  for an ``int`` field.
* The document marks no response field required, so response scalars decode as-is while
  containers (arrays, nested objects) default to ``None`` — an empty collection can come back
  as an omitted key, and ``from_dict`` raises for a declared field the payload omits.

Sub-packages:

* :mod:`tcbs_api.dto.account` — profile information for a sub-account
* :mod:`tcbs_api.dto.auth` — the JWT token response
* :mod:`tcbs_api.dto.money` — cash transfers, margin deposit and withdrawal
* :mod:`tcbs_api.dto.stock_normal` — stock orders, purchasing power, assets and cash
* :mod:`tcbs_api.dto.market` — cash-market price board, foreign room, supply and demand
* :mod:`tcbs_api.dto.derivative` — derivatives cash, positions, orders and market data
"""

from __future__ import annotations

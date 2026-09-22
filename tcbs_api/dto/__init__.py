"""Response models, grouped by API domain.

Every model is a pydantic v2 model whose field names match the JSON keys TCBS sends, keeping
their original camelCase — ``OrderDetail.orderID`` and ``CashInvestmentInfo.pp0forBF`` are
spelled the way the API spells them rather than the way Python normally would. That keeps the
mapping between code and API payloads obvious, and is why responses decode straight onto these
classes. A key that is *not* a legal Python name carries its spelling as ``Field(alias=...)``
instead — ``PriceMatchingInfo.as_`` is the one example so far.

Parsing leans lenient. Fields hold defaults where the API may omit them and unknown keys are
ignored, so a response carrying something new is not an error; a payload that does not fit the
model — a required field missing, a value that cannot be coerced — raises pydantic's
``ValidationError``.

Every model starts from the fields TCBS's OpenAPI document declares for its operation, but the
document is wrong, thin or silent often enough that fifteen of the nineteen operations were
corrected against live payloads — the README's *Known limitations* has the per-operation table,
and ``tests/integration_test.py`` reports the drift whenever it reappears.

An annotation is the intended type, and pydantic's lax mode gets most payloads there: the quoted
``"30500"`` lands in a ``float`` field as ``30500.0``. A value it cannot read is a
``ValidationError`` rather than a silently wrong object.

A field always carries a description, so ``model_json_schema()`` documents the model. Where the
text comes from, in order: the OpenAPI document's own wording; 5.11's documentation page, which is
hand-written because the document declares no response there at all; and the captured payloads for
everything the document leaves out. A field nothing explains says so — ``rcp`` and ``pcp`` in 5.5,
5.4's ``color``, 5.7's ``d``, the null-valued fields 5.5 sends, and the handful of 4.14 counters
whose meaning only TCBS knows — rather than inventing one.

Sub-packages:

* `tcbs_api.dto.base` — the pydantic base class every model inherits
* `tcbs_api.dto.account` — profile information for a sub-account
* `tcbs_api.dto.token` — the JWT token response
* `tcbs_api.dto.stock` — stock orders, purchasing power, assets and cash
* `tcbs_api.dto.market` — cash-market price board, foreign room, supply and demand
"""

from __future__ import annotations

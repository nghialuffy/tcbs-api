# Errors and validation

Nothing is swallowed: a failed HTTP call raises, and so does a payload that does not fit its
model.

## HTTP failures

Non-2xx responses go through `requests.Response.raise_for_status()`, so HTTP failures surface as
`requests.HTTPError`:

```python
import requests

from tcbs_api.service import stock as stock_service

try:
    orders = stock_service.get_orders(account_no="0001201435", token=token)
except requests.HTTPError as exc:
    print(exc.response.status_code, exc.response.json())
```

The library performs no retries, rate limiting or token refresh, and it does not translate the
error — `exc.response` is the real one, status code, headers and body included. Deciding what to
do about a 401 (refresh the token) or a 429 (back off) is the caller's policy. See
[Operational notes](../limitations.md#operational-notes).

## Payloads that do not fit

`decode` is a thin `model_validate`, so a response that does not match its model — a required
field missing, a value that cannot be coerced — raises pydantic's `ValidationError` rather than
handing back a half-built object:

```python
from pydantic import ValidationError

from tcbs_api.service import market as market_service

try:
    response = market_service.get_foreign_room(token, index=1)
except ValidationError as exc:
    print(exc.errors())  # [{'loc': ('data', 0, 'matchPrice'), 'msg': 'Input should be a valid number', ...}]
```

`exc.errors()` names the offending field path and what arrived instead, which is what makes a
`ValidationError` worth reporting upstream: it means the API changed shape, not that the request
was wrong.

### A narrow `fields` can under-fill a model

The models for operation 5.11 describe the full (`fields=all`) projection. Requesting a narrower
projection narrows the **response** too, so `fields=symbol` leaves the required listing fields
missing and raises a `ValidationError` naming them. Narrow `fields` only as far as the model can
still be filled in:

```python
market_service.get_securities_info(token, filter_expression="symbol=TCB")  # fine — fields=all
```

## What is tolerated

Parsing leans lenient, so a payload carrying something new is not an error:

- **Unknown keys are ignored.** A column TCBS adds never breaks a call. Only a *changed* type or
  a missing required field is worth reporting.
- **Omitted fields fall back to their defaults** — as long as the model declares them optional,
  which is why `orders`, `data`, `stock`, `response` and friends are `None` when the API omits
  them. Read those with `or []`.
- **Nothing is coerced beyond pydantic's lax mode.** `"30500"` lands in a `float` field as
  `30500.0`, which is how 5.3's quoted prices and 5.11's `newPrice` read as numbers; anything
  that may be fractional is a `float` rather than an `int` for the same reason.

Fields whose JSON type no live value pinned down stay `Any`: `avatarData`, `personalBasicInfo`,
an `rmRefInfo` item, 5.3's `sellForeignQtty`, 5.5's `pcps`/`hc`/`ac`/`pcpc` and `as_`, 5.4's
`color`, and 5.7's `d`.

## Getting the payload back out

Every model is a pydantic v2 model, so `model_dump` gets you plain data again:

```python
response.model_dump()  # field names
response.model_dump(by_alias=True)  # JSON keys — "as" rather than "as_"
```

## A key that is not a Python name

5.5's `as` key is a Python keyword, so the field is `as_` and carries the JSON spelling as a
pydantic alias:

```python
from typing import Any

from pydantic import Field

as_: Any = Field(default=None, alias="as")
```

Every model sets `populate_by_name`, so `row.as_` and `Row(as_=…)` work as well as the payload's
`as` key, and `model_dump(by_alias=True)` writes `as` back out. It is the only such field so far.

## Next

- [Known limitations](../limitations.md) — what is not wrapped, and where the models beat the
  document
- [`tcbs_api.utils.request_api`](../api/support.md#tcbs_api.utils.request_api) — the layer that does all of this

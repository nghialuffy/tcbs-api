# tcbs-api

Python client library for the [TCBS Open API](https://developers.tcbs.com.vn/).

`tcbs-api` is a thin, dependency-light wrapper over the TCBS REST **read** endpoints:
authentication, account information, stock order and trade lookups, holdings, cash, and
cash-market data. Responses are parsed into typed [pydantic](https://docs.pydantic.dev/)
models, so you get autocompletion and real attributes instead of hand-written `dict` poking.

- Distribution name: `tcbs-api`
- Import package: `tcbs_api`
- Source code: <https://github.com/nghialuffy/tcbs-api>
- Issue tracker: <https://github.com/nghialuffy/tcbs-api/issues>
- Official API docs: <https://developers.tcbs.com.vn/>
- Requires: Python 3.10 or newer, and a TCBS Open API key

## Install

```bash
uv add tcbs-api
```

Or with pip:

```bash
pip install tcbs-api
```

See [Installation](getting-started/installation.md) for the other ways to install it.

## A first call

```python
from tcbs_api.service import token as token_service

# 1.1. Exchange the API key for a JWT token. Rate limited to 10 requests/day — persist it.
token = token_service.get_token("your-api-key", "your-otp").token

# Every other call takes that token as its last positional argument.
```

The [Quick start](getting-started/quickstart.md) takes it from there — account information,
holdings, cash and market data.

## What is covered

| Module | Covers |
| --- | --- |
| [`tcbs_api.service.token`](api/services.md#tcbs_api.service.token) | Exchange an API key for a JWT token (1.1) |
| [`tcbs_api.service.account`](api/services.md#tcbs_api.service.account) | Account information (2.1) |
| [`tcbs_api.service.stock`](api/services.md#tcbs_api.service.stock) | Stock orders, trades, purchasing power, holdings, cash balance and cash statement (4.x) |
| [`tcbs_api.service.market`](api/services.md#tcbs_api.service.market) | Cash-market price board, foreign room, put-through, intraday and supply-and-demand data (5.x) |

Request and response models live under [`tcbs_api.dto`](api/models.md#tcbs_api.dto), grouped by the same
domains. The public API mirrors the numbering used in the TCBS documentation: operation 4.14,
for instance, is
[`get_asset_stock_by_sub_account`](api/services.md#tcbs_api.service.stock.get_asset_stock_by_sub_account).


!!! note "Nothing here writes"

    The nine endpoints that place, amend or cancel an order — and the three that move cash —
    are deliberately not wrapped, so no function in this library changes anything at TCBS.
    `get_token` is the only call that issues a `POST`, and it only exchanges the API key for a
    token. See [Known limitations](limitations.md).

## Design

**One function per endpoint.** Every function is a thin declaration of one operation — its
URL, HTTP verb, query parameters and response model. The request plumbing (base URL, bearer
headers, status check, decoding) is written once in
[`tcbs_api.utils.request_api`](api/support.md#tcbs_api.utils.request_api).

**Typed responses.** Payloads decode onto pydantic models whose field names keep TCBS's own
camelCase spelling, so code and API payload line up exactly. Every field carries a
description, which is what makes the [API reference](api/index.md) explain the payloads
rather than just list names.

**Lenient by default, loud on real mismatches.** Unknown keys are ignored and omitted fields
fall back to their defaults; a payload that genuinely does not fit raises pydantic's
`ValidationError` instead of handing back a half-built object — see
[Errors and validation](guides/errors-and-validation.md).

## Next steps

- [Installation](getting-started/installation.md)
- [Quick start](getting-started/quickstart.md)
- [Guides](guides/account-information.md) — account information, holdings and cash, market data
- [API reference](api/index.md)
- [Known limitations](limitations.md)

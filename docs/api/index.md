# API reference

This reference is generated from the package: mkdocstrings reads the signatures, the type
annotations, the docstrings and the `Field(description=…)` text of every model, so it always
describes the code that is installed. Every public function, model and field is listed.

## Services

One module per API domain, one function per endpoint.

| Module | Covers |
| --- | --- |
| `tcbs_api.service.token` | Exchange an API key for a JWT token (1.1) |
| `tcbs_api.service.account` | Account information (2.1) |
| `tcbs_api.service.stock` | Stock orders, trades, purchasing power, holdings, cash balance and cash statement (4.x) |
| `tcbs_api.service.market` | Cash-market price board, foreign room, put-through, intraday and supply-and-demand data (5.x) |

Full signatures are on [Services](services.md); start with the
[Quick start](../getting-started/quickstart.md) for the call patterns, or with the guides —
[Account information](../guides/account-information.md),
[Holdings and cash](../guides/holdings-and-cash.md),
[Market data](../guides/market-data.md) — for what each endpoint returns.

## Models

Request and response models, grouped by the same domains.

| Module | Holds |
| --- | --- |
| `tcbs_api.dto.token` | The token response |
| `tcbs_api.dto.account` | Profile blocks of a sub-account |
| `tcbs_api.dto.stock` | Orders, matches, purchasing power, holdings, cash |
| `tcbs_api.dto.market` | Price board, foreign room, put-through, supply and demand, securities |

Every field of every model is described on [Models](models.md).

## Support

The base URL and the request layer every service call funnels through, on [Support](support.md).

## How to read a signature

Two call shapes, and the rule behind them: **`token` is the last positional argument unless every
other argument is an optional filter**, in which case it comes first and the filters are
keyword-only. A filter left as `None` never reaches the query string — `requests` drops `None`
parameters — which is what keeps the endpoints' own defaults in play.

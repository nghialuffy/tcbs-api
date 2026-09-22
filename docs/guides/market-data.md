# Market data

The 5.x cash-market endpoints live under
[`tcbs_api.service.market`](../api/services.md#tcbs_api.service.market). This is read-only market data, so
`token` is still required — an API key buys access to the market feed too.

```python
from tcbs_api.service import market as market_service
```

!!! note "The live price board is a WebSocket"

    TCBS publishes the streaming board as a WebSocket (section 5.2), which this library does not
    cover. The endpoints here are the REST snapshots and series.

## Argument order

Where the endpoint has a symbol of its own, the token stays last:

```python
market_service.get_supply_demand_daily("FPT", token, investor_type="shark")
```

Where everything except the token is an optional filter, the token comes first and the filters
are keyword-only:

```python
market_service.get_symbol_and_price(token, index=1)
```

## Basket and floor codes

`index` selects a basket:

| `index` | Basket | `index` | Basket |
| --- | --- | --- | --- |
| 1 | HOSE | 13 | VNSmallCap |
| 2 | VN30 | 14 | VNXAllShare |
| 3 | HNX | 15 | VN50 |
| 4 | HNX30 | 16 | VNSI |
| 5 | UPCOM | | |
| 10 | Midcap | | |
| 11 | VN100 | | |
| 12 | VNAllShare | | |

`floor` selects a single exchange: 1 = HOSE, 2 = HNX, 3 = UPCOM.

## Investor classes

`investor_type` filters the supply-and-demand series:

| Value | Investor class |
| --- | --- |
| `"sheep"` | Small retail |
| `"wolf"` | Medium institutional |
| `"shark"` | Large institutional |
| `"all"`, or omitted | Every class |

## Symbol and price board (5.1)

```python
board = market_service.get_symbol_and_price(token, index=1)
print(board.tradingDate, len(board.data))
print(board.data[0].symbol, board.data[0].matchPrice, board.data[0].totalVol)
```

A basket by `index`, or an explicit list by `tickers` — TCBS documents the two as mutually
exclusive, so pass one or the other:

```python
board = market_service.get_symbol_and_price(token, tickers="FPT,TCB,SSI")
```

Each row is a [`SymbolPriceInfo`](../api/models.md#tcbs_api.dto.market). Outside trading hours the endpoint omits
most of the board fields, leaving `symbol` as the only guaranteed one, so read prices with a
fallback in mind.

## Foreign room (5.3)

```python
room = market_service.get_foreign_room(token, index=1)
row = room.data[0]
print(row.symbol, row.buyForeignQtty, row.room, row.matchPrice)
```

Each row is the full price board plus the foreign-ownership figures — 28 keys where the document
declares 13, and the response carries no `tradingDate`. Every price and quantity in these rows
comes **quoted** (`"30500"`), which pydantic reads into the `float` fields as `30500.0`. A few
keys are absent for some symbols, so those fields are optional.

## Put-through (5.4)

```python
deals = market_service.get_put_through(token, floor=1)
for order in deals.buyAdv or []:
    print(order.symbol, order.price, order.vol, order.side)
for match in deals.match or []:
    print(match.time, match.symbol, match.price, match.vol, match.val)
```

Per-exchange (`floor`) negotiated deals, in three lists: advertised buy orders (`buyAdv`),
advertised sell orders (`sellAdv`) and actual matches (`match`). TCBS documents the rows of each
list but never the lists themselves, so all three are optional.

## Price history (5.5)

```python
history = market_service.get_price_matching_history("FPT", token, page=0, size=100)
for match in history.data:
    print(match.t, match.p, match.v, match.a, match.as_)  # `p` is the price, `as_` the `as` field
```

Match-by-match intraday history for one symbol. Pages are numbered from 0 and `size` is capped
at 100 by TCBS. `head_index` (`headIndex` on the wire) drives reverse paging and defaults to -1
server-side, so leaving it out takes that default.

Rows carry more than the document declares — including `rcp`/`pcp` and the `as` field, which is
a Python keyword and is therefore exposed as
[`as_`](errors-and-validation.md#a-key-that-is-not-a-python-name) — and the response closes with
the trading date in `d`. The paging counters (`page`, `size`, `numberOfItems`, `total`) are
documented as doubles, hence `float`.

## Supply and demand (5.6, 5.7, 5.8)

The daily series is the simplest:

```python
flow = market_service.get_supply_demand_daily("FPT", token, investor_type="shark")
print(flow.data[-1].t, flow.data[-1].bsr, flow.data[-1].bup, flow.data[-1].sdp)
```

Each point is a bucket — a date for the daily and monthly series, a time for the intraday one —
carrying the buy-up and sell-down percentages and the buy/sell ratio `bsr` between them.

The intraday series additionally comes in 15- or 60-minute buckets, with a moving-sum window on
top:

```python
intraday = market_service.get_supply_demand_intraday("FPT", time_window=15, t_window=15, token=token)
```

`time_window` (`timeWindow`) is the bucket size in minutes — 15 or 60 — and `t_window`
(`tWindow`) is the window the moving sums are taken over, which TCBS documents only as 15. Its
rows are shaped differently from the daily ones ([`SupplyDemandIntradayInfo`](../api/models.md#tcbs_api.dto.market)
against [`SupplyDemandPoint`](../api/models.md#tcbs_api.dto.market)): absolute buy-up and sell-down volumes with
their moving sums, rather than percentages alone.

The monthly series takes an optional `time_window` of `"1M"`, the only value TCBS documents:

```python
monthly = market_service.get_supply_demand_monthly("FPT", token, time_window="1M")
```

## Securities lookup (5.11)

```python
securities = market_service.get_securities_info(token, filter_expression="symbol=TCB")
for row in securities.content or []:
    listing = row.securitiesInfo
    print(row.symbol, row.tradePlace, row.parValue, listing.listingQtty, listing.basicPrice)
```

`fields` projects the fields to return (`fields=all`, or omitted entirely, returns everything)
and `filter_expression` is an expression in `field=value` form. This endpoint has no response in
the OpenAPI document at all, so the models follow a captured payload: a page of `content` rows,
each with a 36-field `securitiesInfo` block, plus the `pageable`/`sort` blocks Spring echoes
back.

Because those models describe the **full** projection, a narrow `fields` only works as far as the
model can still be filled in — narrowing too far raises a `ValidationError` naming what is
missing. See [Errors and validation](errors-and-validation.md).

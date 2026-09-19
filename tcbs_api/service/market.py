"""Cash-market data: price board, foreign room, put-through, intraday and supply and demand.

Every function here is a thin declaration of one endpoint — the URL, the verb, the query
parameters and the response DTO. The request plumbing lives in
:mod:`tcbs_api.utils.request_api`.

``token`` is the last positional argument except where every other argument is an optional
filter: Python rejects a required parameter after a defaulted one, so those functions take
``token`` first and their filters as keyword-only arguments defaulting to ``None``. A
``None`` filter never reaches the query string, which is what ``requests`` does with it.

The ``index`` parameter of the board endpoints selects a basket: 1 = HOSE, 2 = VN30,
3 = HNX, 4 = HNX30, 5 = UPCOM, 10 = Midcap, 11 = VN100, 12 = VNAllShare, 13 = VNSmallCap,
14 = VNXAllShare, 15 = VN50, 16 = VNSI.

``investor_type`` (the ``type`` parameter) filters the supply-and-demand series by investor
class: "sheep" (small retail), "wolf" (medium institutional), "shark" (large institutional),
or "all" when omitted.
"""

from __future__ import annotations

from tcbs_api.dto import market
from tcbs_api.utils import request_api


def get_symbol_and_price(
    token: str,
    *,
    tickers: str | None = None,
    index: int | None = None,
) -> market.SymbolPriceResponse:
    """Get the symbol and price board of the cash market.

    Operation 5.1 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/market-symbol/

    `tickers` is a comma-separated list of symbols and `index` a basket (codes in the
    module docstring). TCBS documents the two as mutually exclusive — pass one or the
    other. The live price board is the WebSocket in section 5.2, which this library does
    not cover.
    """
    payload = request_api.get(
        "/tartarus/v1/tickerCommons",
        token,
        params={"tickers": tickers, "index": index},
    )
    return request_api.decode(market.SymbolPriceResponse, payload)


def get_foreign_room(token: str, *, index: int | None = None) -> market.ForeignRoomResponse:
    """Get the foreign-ownership room and market snapshot of a stock basket.

    Operation 5.3 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/foreign-room/

    `index` picks the basket — codes in the module docstring.

    Each row is the full price board plus the foreign figures, with every price and quantity
    quoted as a string — see :class:`~tcbs_api.dto.market.ForeignRoomInfo`.
    """
    payload = request_api.get("/tartarus/v1/tickerSnaps", token, params={"index": index})
    return request_api.decode(market.ForeignRoomResponse, payload)


def get_put_through(token: str, *, floor: int | None = None) -> market.PutThroughResponse:
    """Get put-through (negotiated deal) orders and matches.

    Operation 5.4 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/put-through/

    `floor` selects the exchange: 1 = HOSE, 2 = HNX, 3 = UPCOM.
    """
    payload = request_api.get("/tartarus/v1/putThroughSnaps", token, params={"floor": floor})
    return request_api.decode(market.PutThroughResponse, payload)


def get_price_matching_history(
    ticker: str,
    token: str,
    *,
    page: int | None = None,
    size: int | None = None,
    head_index: int | None = None,
) -> market.PriceMatchingHistoryResponse:
    """Get the intraday match-by-match price history of one symbol.

    Operation 5.5 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/price-history/

    Pages are numbered from 0 and `size` is capped at 100 by TCBS. `head_index` (`headIndex`
    on the wire) serves reverse paging and defaults to -1 server-side, so leaving it out
    takes that default.

    Each row carries more than the document declares — see
    :class:`~tcbs_api.dto.market.PriceMatchingInfo` — and the response closes with the
    trading date in ``d``.
    """
    payload = request_api.get(
        f"/nyx/v1/intraday/{ticker}/his/paging",
        token,
        params={"page": page, "size": size, "headIndex": head_index},
    )
    return request_api.decode(market.PriceMatchingHistoryResponse, payload)


def get_supply_demand_intraday(
    ticker: str,
    time_window: int,
    t_window: int,
    token: str,
    *,
    investor_type: str | None = None,
) -> market.SupplyDemandIntradayResponse:
    """Get the intraday supply-and-demand series of one symbol, in 15-minute buckets.

    Operation 5.6 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/supply-demand-intraday/

    `time_window` (`timeWindow`) is the bucket size in minutes — 15 or 60 — and `t_window`
    (`tWindow`) the window the moving sums are taken over, which TCBS documents only as 15.
    `investor_type` picks the investor class — see the module docstring.
    """
    payload = request_api.get(
        f"/nyx/v1/intraday/{ticker}/bsa-ext",
        token,
        params={"timeWindow": time_window, "tWindow": t_window, "type": investor_type},
    )
    return request_api.decode(market.SupplyDemandIntradayResponse, payload)


def get_supply_demand_daily(
    ticker: str,
    token: str,
    *,
    investor_type: str | None = None,
) -> market.SupplyDemandDailyResponse:
    """Get the daily supply-and-demand series of one symbol.

    Operation 5.7 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/supply-demand-daily/

    `investor_type` picks the investor class — see the module docstring.
    """
    payload = request_api.get(
        f"/nyx/v1/intraday/{ticker}/bsa",
        token,
        params={"type": investor_type},
    )
    return request_api.decode(market.SupplyDemandDailyResponse, payload)


def get_supply_demand_monthly(
    ticker: str,
    token: str,
    *,
    time_window: str | None = None,
    investor_type: str | None = None,
) -> market.SupplyDemandMonthlyResponse:
    """Get the monthly supply-and-demand series of one symbol.

    Operation 5.8 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/supply-demand-monthly/

    `time_window` (`timeWindow`) is "1M", the only value TCBS documents, and is optional
    because the server treats it as the default. `investor_type` picks the investor class —
    see the module docstring.
    """
    payload = request_api.get(
        f"/nyx/v1/intraday/{ticker}/bsa-month",
        token,
        params={"timeWindow": time_window, "type": investor_type},
    )
    return request_api.decode(market.SupplyDemandMonthlyResponse, payload)


def get_securities_info(
    token: str,
    *,
    fields: str | None = None,
    filter_expression: str | None = None,
) -> market.SecuritiesResponse:
    """Look up listing data for the securities TCBS knows about.

    Operation 5.11 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/securities-info/

    `fields` is a projection of the fields to return and `filter_expression` (the ``filter``
    parameter) is an expression in ``field=value`` form, e.g. ``symbol=TCB``. Called with
    neither, the endpoint returns every field of every security.

    The OpenAPI document declares no response at all for this operation, so
    :class:`~tcbs_api.dto.market.SecuritiesResponse` and its nested models are derived from a
    real payload. That payload is a page of ``content`` rows, each with a ``securitiesInfo``
    block holding the listing prices and limits.

    Those models describe the full projection — ``fields=all``, or no ``fields`` at all — so
    narrow ``fields`` only as far as the model can still be filled in.
    """
    payload = request_api.get(
        "/ananke/v1/securities",
        token,
        params={"fields": fields, "filter": filter_expression},
    )
    return request_api.decode(market.SecuritiesResponse, payload)

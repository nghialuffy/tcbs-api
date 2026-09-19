"""Cash-market data models: price board, foreign room, put-through, intraday supply and demand.

Field names keep the camelCase spelling TCBS uses, and types follow the document's; the
typing and optionality rules shared by every model live in :mod:`tcbs_api.dto`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SymbolPriceInfo:
    """One row of the 5.1 price board."""

    symbol: str
    ceilPrice: float
    floorPrice: float
    refPrice: float
    matchPrice: float
    totalVol: float
    bidPrice01: float | None = None
    bidPrice02: float | None = None
    bidPrice03: float | None = None
    bidQtty01: float | None = None
    bidQtty02: float | None = None
    bidQtty03: float | None = None
    offerPrice01: float | None = None
    offerPrice02: float | None = None
    offerPrice03: float | None = None
    offerQtty01: float | None = None
    offerQtty02: float | None = None
    offerQtty03: float | None = None
    matchQtty: float | None = None
    change: float | None = None
    changePercent: float | None = None
    open: float | None = None
    high: float | None = None
    low: float | None = None
    avg: float | None = None
    totalVal: float | None = None
    buyForeignQtty: float | None = None
    sellForeignQtty: float | None = None
    room: float | None = None
    indexNumber: float | None = None


@dataclass
class SymbolPriceResponse:
    """Response of ``get_symbol_and_price`` (operation 5.1)."""

    data: list[SymbolPriceInfo]
    tradingDate: str


@dataclass
class ForeignRoomInfo:
    """One row of the 5.3 foreign-room snapshot."""

    symbol: str
    refPrice: float
    ceilPrice: float
    floorPrice: float
    matchPrice: float
    matchQtty: float
    change: float
    changePercent: float
    totalVolume: float
    totalValue: float
    buyForeignQtty: float
    sellForeignQtty: float
    room: str


@dataclass
class ForeignRoomResponse:
    """Response of ``get_foreign_room`` (operation 5.3)."""

    tradingDate: str
    data: list[ForeignRoomInfo]


@dataclass
class PutThroughAdvOrder:
    """One advertised (unmatched) put-through order, from ``buyAdv`` or ``sellAdv``.

    ``time`` is optional because TCBS lists it for the buy side only; a sell-side row may
    simply not carry it.
    """

    symbol: str
    price: float
    vol: float
    side: str
    time: str | None = None


@dataclass
class PutThroughMatch:
    """One matched put-through deal."""

    symbol: str
    price: float
    vol: float
    val: float
    time: str
    accumulatedValue: float


@dataclass
class PutThroughResponse:
    """Response of ``get_put_through`` (operation 5.4).

    TCBS documents the rows of each list but never the lists themselves, so all three are
    optional and a response that leaves one out decodes to ``None``.
    """

    buyAdv: list[PutThroughAdvOrder] | None = None
    sellAdv: list[PutThroughAdvOrder] | None = None
    match: list[PutThroughMatch] | None = None


@dataclass
class PriceMatchingInfo:
    """One match of the 5.5 intraday price history."""

    p: float
    v: float
    cp: float
    a: str
    ba: float
    sa: float
    hl: bool
    t: str


@dataclass
class PriceMatchingHistoryResponse:
    """Response of ``get_price_matching_history`` (operation 5.5).

    The paging counters are documented as doubles, hence ``float``.
    """

    page: float
    size: float
    headIndex: float
    numberOfItems: float
    total: float
    ticker: str
    data: list[PriceMatchingInfo]


@dataclass
class SupplyDemandIntradayInfo:
    """One 15-minute bucket of the 5.6 supply-and-demand series."""

    bu: float
    bms: float
    bup: float
    sd: float
    sms: float
    sdp: float
    bsr: float
    t: str
    s: float


@dataclass
class SupplyDemandIntradayResponse:
    """Response of ``get_supply_demand_intraday`` (operation 5.6)."""

    ticker: str
    data: list[SupplyDemandIntradayInfo]


@dataclass
class SupplyDemandPoint:
    """One bucket of a daily or monthly supply-and-demand series.

    Operations 5.7 and 5.8 return rows of the same shape, so they share this model.
    """

    bup: float
    sdp: float
    bsr: float
    t: str


@dataclass
class SupplyDemandDailyResponse:
    """Response of ``get_supply_demand_daily`` (operation 5.7)."""

    ticker: str
    data: list[SupplyDemandPoint]


@dataclass
class SupplyDemandMonthlyResponse:
    """Response of ``get_supply_demand_monthly`` (operation 5.8)."""

    ticker: str
    data: list[SupplyDemandPoint]

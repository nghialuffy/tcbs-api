"""Cash-market data models: price board, foreign room, put-through, intraday supply and demand.

Field names keep the camelCase spelling TCBS uses, and types follow the document's; the
typing and optionality rules shared by every model live in :mod:`tcbs_api.dto`.

Three endpoints here are modelled from real payloads instead: 5.3 and 5.5, whose rows carry
fields the document never declares, and 5.11, for which the document declares no response at
all.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from tcbs_api.dto.base import DtoModel


class SymbolPriceInfo(DtoModel):
    """One row of the 5.1 price board."""

    symbol: str = Field(description="Stock symbol.")
    ceilPrice: float | None = Field(default=None, description="Ceiling price.")
    floorPrice: float | None = Field(default=None, description="Floor price.")
    refPrice: float | None = Field(default=None, description="Reference price.")
    matchPrice: float | None = Field(default=None, description="Matched price.")
    totalVol: float | None = Field(default=None, description="Total trading volume.")
    bidPrice01: float | None = Field(default=None, description="Bid price 1.")
    bidPrice02: float | None = Field(default=None, description="Bid price 2.")
    bidPrice03: float | None = Field(default=None, description="Bid price 3.")
    bidQtty01: float | None = Field(default=None, description="Bid volume 1.")
    bidQtty02: float | None = Field(default=None, description="Bid volume 2.")
    bidQtty03: float | None = Field(default=None, description="Bid volume 3.")
    offerPrice01: float | None = Field(default=None, description="Offer price 1.")
    offerPrice02: float | None = Field(default=None, description="Offer price 2.")
    offerPrice03: float | None = Field(default=None, description="Offer price 3.")
    offerQtty01: float | None = Field(default=None, description="Offer volume 1.")
    offerQtty02: float | None = Field(default=None, description="Offer volume 2.")
    offerQtty03: float | None = Field(default=None, description="Offer volume 3.")
    matchQtty: float | None = Field(default=None, description="Matched volume.")
    change: float | None = Field(default=None, description="Price change.")
    changePercent: float | None = Field(default=None, description="Change percent.")
    open: float | None = Field(default=None, description="Open price.")
    high: float | None = Field(default=None, description="High price.")
    low: float | None = Field(default=None, description="Low price.")
    avg: float | None = Field(default=None, description="Average price.")
    totalVal: float | None = Field(default=None, description="Total trading value.")
    buyForeignQtty: float | None = Field(default=None, description="Foreign buy volume.")
    sellForeignQtty: float | None = Field(default=None, description="Foreign sell volume.")
    room: float | None = Field(default=None, description="Foreign room.")
    indexNumber: float | None = Field(default=None, description="Stock basket index.")
    nextCeilPrice: float | None = Field(default=None, description="Ceiling price for the next session.")
    nextFloorPrice: float | None = Field(default=None, description="Floor price for the next session.")
    nextRefPrice: float | None = Field(default=None, description="Reference price for the next session.")


class SymbolPriceResponse(DtoModel):
    """Response of ``get_symbol_and_price`` (operation 5.1)."""

    data: list[SymbolPriceInfo] = Field(description="List of ticker information.")
    tradingDate: str = Field(description="Trading date (dd/MM/yyyy).")


class ForeignRoomInfo(DtoModel):
    """One row of the 5.3 basket snapshot — the price board plus the foreign-ownership room.

    The API quotes every price, quantity and amount as a string (``"32600"``); pydantic's lax
    mode turns those into the ``float`` fields here, so the row reads as numbers even though 5.1
    sends the same figures unquoted.

    ``sellForeignQtty`` is declared by the document but absent from the sampled payload, and the
    payload quotes the sibling ``buyForeignQtty`` while the document calls both ``number``, so
    its JSON type is unconfirmed and it stays ``Any``.
    """

    symbol: str = Field(description="Stock symbol.")
    ceilPrice: float | None = Field(default=None, description="Ceiling price.")
    floorPrice: float | None = Field(default=None, description="Floor price.")
    refPrice: float | None = Field(default=None, description="Reference price.")
    bidPrice01: float | None = Field(default=None, description="Bid price level 1.")
    bidPrice02: float | None = Field(default=None, description="Bid price level 2.")
    bidPrice03: float | None = Field(default=None, description="Bid price level 3.")
    bidQtty01: float | None = Field(default=None, description="Bid volume level 1.")
    bidQtty02: float | None = Field(default=None, description="Bid volume level 2.")
    bidQtty03: float | None = Field(default=None, description="Bid volume level 3.")
    offerPrice01: float | None = Field(default=None, description="Offer price level 1.")
    offerPrice02: float | None = Field(default=None, description="Offer price level 2.")
    offerPrice03: float | None = Field(default=None, description="Offer price level 3.")
    offerQtty01: float | None = Field(default=None, description="Offer volume level 1.")
    offerQtty02: float | None = Field(default=None, description="Offer volume level 2.")
    offerQtty03: float | None = Field(default=None, description="Offer volume level 3.")
    matchPrice: float | None = Field(default=None, description="Matched price.")
    matchQtty: float | None = Field(default=None, description="Matched volume.")
    change: float | None = Field(default=None, description="Price change.")
    changePercent: float | None = Field(default=None, description="Change percent.")
    avg: float | None = Field(default=None, description="Average match price.")
    high: float | None = Field(default=None, description="Highest match price.")
    low: float | None = Field(default=None, description="Lowest match price.")
    totalValue: float | None = Field(default=None, description="Total value.")
    totalVolume: float | None = Field(default=None, description="Total volume.")
    buyForeignQtty: float | None = Field(default=None, description="Foreign buy volume.")
    room: float | None = Field(default=None, description="Foreign room.")
    open: float | None = Field(default=None, description="Opening price.")
    sellForeignQtty: Any = Field(default=None, description="Foreign sell volume.")


class ForeignRoomResponse(DtoModel):
    """Response of ``get_foreign_room`` (operation 5.3).

    The sampled payload carries only ``data``; the document's ``tradingDate`` is optional here
    so that a response without it still decodes.
    """

    tradingDate: str | None = Field(default=None, description="Trading date.")
    data: list[ForeignRoomInfo] | None = Field(default=None, description="One row per security in the basket.")


class PutThroughAdvOrder(DtoModel):
    """One advertised (unmatched) put-through order, from ``buyAdv`` or ``sellAdv``.

    ``time`` is optional because TCBS lists it for the buy side only; a sell-side row may
    simply not carry it.
    """

    symbol: str = Field(description="Stock symbol.")
    price: float = Field(description="Price.")
    vol: float = Field(description="Volume.")
    side: str = Field(description="Side (S = Sell).")
    time: str | None = Field(default=None, description="Time.")


class PutThroughMatch(DtoModel):
    """One matched put-through deal."""

    symbol: str = Field(description="Stock symbol.")
    price: float = Field(description="Matched price.")
    vol: float = Field(description="Matched volume.")
    val: float = Field(description="Value.")
    time: str = Field(description="Match time.")
    accumulatedValue: float = Field(description="Accumulated value.")
    color: Any = Field(
        default=None,
        description="Not documented by TCBS; the live payload sends a value whose type is unconfirmed.",
    )


class PutThroughResponse(DtoModel):
    """Response of ``get_put_through`` (operation 5.4).

    TCBS documents the rows of each list but never the lists themselves, so all three are
    optional and a response that leaves one out decodes to ``None``.
    """

    buyAdv: list[PutThroughAdvOrder] | None = Field(
        default=None,
        description="Advertised buy orders that have not matched yet.",
    )
    sellAdv: list[PutThroughAdvOrder] | None = Field(
        default=None,
        description="Advertised sell orders that have not matched yet.",
    )
    match: list[PutThroughMatch] | None = Field(default=None, description="Matched put-through deals.")


class PriceMatchingInfo(DtoModel):
    """One match of the 5.5 intraday price history.

    The document declares the first eight fields; a real payload also carries ``rcp``/``pcp``
    (reference-price change and its percentage) and five keys that are null for a plain match —
    ``as``, ``pcps``, ``hc``, ``ac`` and ``pcpc`` — whose shapes no sample pinned down, so they
    stay ``Any``. ``as`` is renamed from the JSON key of the same name, which is a Python
    keyword and so cannot be a field name.
    """

    p: float = Field(description="Matching price.")
    v: float = Field(description="Volume.")
    cp: float = Field(description="Price change (price - ref price).")
    rcp: float = Field(description="Not documented by TCBS; 0.0 in every sampled match.")
    a: str = Field(description="Action (Buy up/Sell down).")
    ba: float = Field(description="Buy accumulate.")
    sa: float = Field(description="Sell accumulate.")
    hl: bool = Field(description="Highlight if value > 200M.")
    pcp: float = Field(description="Not documented by TCBS; 0.0 in every sampled match.")
    t: str = Field(description="Time received from exchange.")
    as_: Any = Field(
        description="Not documented by TCBS; null in every sampled match. Carried under the alias as.",
        default=None,
        alias="as",
    )
    pcps: Any = Field(default=None, description="Not documented by TCBS; null in every sampled match.")
    hc: Any = Field(default=None, description="Not documented by TCBS; null in every sampled match.")
    ac: Any = Field(default=None, description="Not documented by TCBS; null in every sampled match.")
    pcpc: Any = Field(default=None, description="Not documented by TCBS; null in every sampled match.")


class PriceMatchingHistoryResponse(DtoModel):
    """Response of ``get_price_matching_history`` (operation 5.5).

    The paging counters are documented as doubles, hence ``float``. ``d`` — the trading date,
    as ``"18/09"`` — is undocumented and follows a real payload.
    """

    page: float = Field(description="Current page.")
    size: float = Field(description="Page size.")
    headIndex: float = Field(description="Head index.")
    numberOfItems: float = Field(description="Number of items returned.")
    total: float = Field(description="Total matched orders.")
    ticker: str = Field(description="Stock symbol.")
    data: list[PriceMatchingInfo] = Field(description="The matches, newest page first.")
    d: str = Field(description="Trading date, e.g. 18/09. Not documented by TCBS.")


class SupplyDemandIntradayInfo(DtoModel):
    """One 15-minute bucket of the 5.6 supply-and-demand series."""

    bu: float = Field(description="Buy Up volume.")
    bms: float = Field(description="Buy Up Moving Sum.")
    bup: float = Field(description="Buy Up Percent.")
    sd: float = Field(description="Sell Down volume.")
    sms: float = Field(description="Sell Down Moving Sum.")
    sdp: float = Field(description="Sell Down Percent.")
    bsr: float = Field(description="Buy/Sell Ratio.")
    t: str = Field(description="Time (HH:mm:ss).")
    s: float = Field(description="Time (timestamp).")


class SupplyDemandIntradayResponse(DtoModel):
    """Response of ``get_supply_demand_intraday`` (operation 5.6)."""

    ticker: str = Field(description="Stock symbol.")
    data: list[SupplyDemandIntradayInfo] = Field(description="The 15-minute buckets, oldest first.")


class SupplyDemandPoint(DtoModel):
    """One bucket of a daily or monthly supply-and-demand series.

    Operations 5.7 and 5.8 return rows of the same shape, so they share this model.
    """

    bup: float = Field(description="Buy Up Percent.")
    sdp: float = Field(description="Sell Down Percent.")
    bsr: float = Field(description="Buy/Sell Ratio.")
    t: str = Field(description="Time (DD/MM).")


class SupplyDemandDailyResponse(DtoModel):
    """Response of ``get_supply_demand_daily`` (operation 5.7)."""

    ticker: str = Field(description="Stock symbol.")
    data: list[SupplyDemandPoint] = Field(description="The daily buckets.")
    d: Any = Field(default=None, description="Trading date. Not documented by TCBS.")


class SupplyDemandMonthlyResponse(DtoModel):
    """Response of ``get_supply_demand_monthly`` (operation 5.8)."""

    ticker: str = Field(description="Stock symbol.")
    data: list[SupplyDemandPoint] = Field(description="The monthly buckets.")


class SecuritiesSort(DtoModel):
    """A ``sort`` block, which 5.11 sends both at the top level and inside ``pageable``."""

    empty: bool = Field(description="Whether the sort list is empty.")
    sorted: bool = Field(description="Whether the results are sorted.")
    unsorted: bool = Field(description="Whether the results are unsorted.")


class SecuritiesListingInfo(DtoModel):
    """The ``securitiesInfo`` block of a 5.11 row: listing quantities, dates, prices and limits.

    Quantities and limits are whole counts, while prices and ratios are ``float`` because they
    may carry decimals. ``newPrice`` is the one number TCBS quotes (``"0"``), which pydantic
    coerces like the rest.
    """

    autoId: int = Field(description="TCBS's internal row id.")
    codeId: str = Field(description="TCBS's code for the security.")
    symbol: str = Field(description="Trading symbol.")
    status: str = Field(
        description="Trading status: 001 = normal, 002 = paused, 003 = stopped, 004 = supervised, 005 = warned.",
    )
    listingQtty: int = Field(description="Total listed quantity.")
    txDate: str = Field(description="Trading date.")
    listingStatus: str = Field(
        description=(
            "Listing status: N = normal, L = newly listed, U = delisted, I = capital increase, D = capital decrease."
        ),
    )
    tradeUnit: int = Field(description="Price unit.")
    adjustQtty: int = Field(description="Quantity the adjustment applies to.")
    listingDate: str = Field(description="Listing date.")
    referenceStatus: str = Field(description="Reference-price status code.")
    adjustRate: float = Field(description="Adjustment rate applied to the price.")
    referenceRate: float = Field(description="Reference rate the price was derived with.")
    referenceDate: str = Field(description="Date the reference price belongs to.")
    ceilingPrice: float = Field(description="Ceiling price.")
    floorPrice: float = Field(description="Floor price.")
    basicPrice: float = Field(description="Reference price.")
    mtmPriceCd: str = Field(description="Mark-to-market price code.")
    pe: float = Field(description="Price/earnings ratio.")
    eps: float = Field(description="Earnings per share.")
    divyeild: float = Field(description="Dividend yield.")
    dayRange: float = Field(description="Daily price range.")
    yearRange: float = Field(description="Yearly price range.")
    tradeLot: int = Field(description="Trade lot size.")
    tradeBuySell: str = Field(description="Same-day buy and sell allowed (Y/N).")
    teleLimitMax: int = Field(description="Maximum order volume by telephone.")
    onlineLimitMax: int = Field(description="Maximum order volume online.")
    repoLimitMax: int = Field(description="Maximum order volume for repo.")
    advancedLimitMax: int = Field(description="Maximum order volume for the advanced order type.")
    marginLimitMax: int = Field(description="Maximum margin trading limit.")
    depoFeeUnit: int = Field(description="Depositary fee per unit.")
    depoFeeLot: int = Field(description="Depositary fee per lot.")
    mortageRatioMax: float = Field(description="Maximum mortgage ratio (TCBS's spelling).")
    securedRatioMin: float = Field(description="Minimum secured ratio.")
    securedRatioMax: float = Field(description="Maximum secured ratio.")
    newPrice: float = Field(description="New price, quoted as a decimal string in the payload.")


class SecuritiesInfo(DtoModel):
    """One row of the 5.11 lookup: a security's header fields plus its listing block.

    ``issuerName``, ``underlyingSymbol`` and ``coveredWarrantType`` are blank-but-present for a
    plain stock — TCBS pads them with spaces rather than sending null. Only the full
    (``fields=all``) projection is modelled; see ``SecuritiesResponse``.
    """

    codeId: str = Field(description="TCBS's code for the security.")
    issuerId: str = Field(description="Issuer identifier.")
    issuerName: str = Field(description="Issuer name — blank (spaces) for a security whose issuer TCBS does not name.")
    symbol: str = Field(description="Trading symbol.")
    secType: str = Field(
        description="Security type: 001 = ordinary share, 002 = preferred share, 003 = convertible bond, 006 = bond.",
    )
    sbType: str = Field(description="Sub-type within secType.")
    investmentType: str = Field(description="Investment term: 001 = short, 002 = long.")
    issueDate: str = Field(description="Issue date.")
    expDate: str = Field(description="Expiry date.")
    underlyingSymbol: str = Field(description="Underlying symbol, for a covered warrant.")
    coveredWarrantType: str = Field(description="Covered-warrant type.")
    exerciseRatio: float = Field(description="Exercise ratio, for a covered warrant.")
    exercisePrice: float = Field(description="Exercise price, for a covered warrant.")
    parValue: float = Field(description="Par value.")
    tradePlace: str = Field(description="Exchange: 001 = HOSE, 002 = HNX, 005 = UPCOM.")
    depository: str = Field(description="Depository the security settles through.")
    bondType: str = Field(description="Bond type, for a bond.")
    marketType: str = Field(description="Market the security belongs to.")
    allowSession: str = Field(description="Trading sessions the security is allowed in.")
    isSeDepofee: str = Field(description="Whether the depositary fee applies (Y/N).")
    intCoupon: float = Field(description="Interest coupon, for a bond.")
    typeTerm: str = Field(description="Unit the term is counted in.")
    term: int = Field(description="Term length, in typeTerm units.")
    status: str = Field(description="In use (Y/N).")
    halt: str = Field(description="Trading halted (Y/N).")
    isinCode: str = Field(description="ISIN code.")
    domain: str = Field(description="Instrument domain, e.g. STCK for a stock.")
    securitiesInfo: SecuritiesListingInfo | None = Field(
        default=None,
        description="The listing detail for this security.",
    )


class SecuritiesPageable(DtoModel):
    """The ``pageable`` block of a 5.11 response."""

    pageNumber: int = Field(description="Zero-based page number.")
    pageSize: int = Field(description="Records per page.")
    offset: int = Field(description="Row offset of this page.")
    paged: bool = Field(description="Whether the results are paged.")
    unpaged: bool = Field(description="Whether the whole result set came back unpaged.")
    sort: SecuritiesSort | None = Field(default=None, description="How the page is sorted.")


class SecuritiesResponse(DtoModel):
    """Response of ``get_securities_info`` (operation 5.11) — a page of securities.

    The OpenAPI document declares no response for this operation, so the shape here follows a
    real payload. The row list and the nested ``sort``/``pageable`` blocks are optional: the
    ``fields`` projection can leave any of them out of the response.

    A row's own scalars, by contrast, are required, so these models describe the full
    (``fields=all``) shape. A projection that drops one — ``fields=symbol``, say — does not
    fit them, and decoding it raises pydantic's ``ValidationError`` rather than filling in
    ``None``.
    """

    last: bool = Field(description="Whether this is the last page.")
    totalElements: int = Field(description="Total records matching the filter.")
    totalPages: int = Field(description="Total pages.")
    size: int = Field(description="Records per page (default 1000).")
    number: int = Field(description="Current page (0-indexed).")
    first: bool = Field(description="Whether this is the first page.")
    numberOfElements: int = Field(description="Records on this page.")
    empty: bool = Field(description="Whether this page has no records.")
    sort: SecuritiesSort | None = Field(default=None, description="How the results are sorted.")
    content: list[SecuritiesInfo] | None = Field(default=None, description="The securities on this page.")
    pageable: SecuritiesPageable | None = Field(default=None, description="The paging request Spring echoes back.")

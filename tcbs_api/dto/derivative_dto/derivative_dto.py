"""Derivatives models, including the envelope that every derivative endpoint returns.

``DerivativeResponse[T]`` is that envelope — ``{cmd, rc, rs, oID, data}``. The response
models used as its ``T`` carry ``@dataclass_json`` so they can be decoded with
``from_json()``; the remaining classes are request bodies, plus two market-information
models that are decoded with ``dacite`` like the rest of the library.

Beware that a field annotated ``Optional[...]`` is not optional at decode time unless it
also has a ``= None`` default — ``from_dict``/``from_json`` raise ``KeyError`` for a field
the API omits. See the README's known limitations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from dataclasses_json import dataclass_json

T = TypeVar("T")


@dataclass_json
@dataclass
class DerivativeResponse(Generic[T]):
    """The ``{cmd, rc, rs, oID, data}`` envelope every derivative endpoint returns.

    ``T`` is the response model for the endpoint. It is not applied at runtime — see this
    module's docstring and the README's known limitations.
    """

    cmd: str
    rc: str
    rs: str
    oID: str
    data: T


@dataclass_json
@dataclass
class TotalCashDerivativeResponse:
    """Derivatives cash, margin and collateral summary."""

    cash: float | None
    stock: float | None
    collateral: float | None
    type: str | None
    net: float | None
    tyle: float | None
    im: float | None
    vm: float | None
    dm: float | None
    mr: float | None
    avaiCash: float | None
    avaiColla: float | None
    vmunpay: float | None
    info: str | None
    color: str | None
    vm_eod: float | None
    others: float | None
    tax: float | None
    feeCTCK: float | None
    feeHNX: float | None
    cashWithdraw: float | None
    tienbosung: float | None
    cashavaiwithdraw: float | None
    assets: float | None
    nav: float | None
    cashOut: float | None
    unrelizeVM: float | None
    feePos: float | None
    feeMan: float | None
    product: str | None
    status: str | None
    debt: float | None
    w1: float | None
    w2: float | None
    limit: float | None
    package: str | None


@dataclass_json
@dataclass
class AssetPositionCloseDerivativeResponse:
    symbol: str
    side: str
    openPrice: float
    closePrice: float
    closePosition: str
    fee: float
    tax: float
    closeVM: float
    unrealize: float
    closePC: float
    time: str


@dataclass_json
@dataclass
class AssetPositionOpenDerivativeResponse:
    symbol: str
    im: str
    deliver: str
    receive: str
    net: int
    side: str
    account: str
    wasp: float
    wapb: float
    lastPrice: float
    imValue: float
    vmValue: float
    mrValue: float
    duedate: str
    netoffvol: int
    avg_remain: float
    vm_remain: float
    pc_remain: str
    stoploss: str | None
    takeprofit: str | None


@dataclass_json
@dataclass
class ListOrderNormalDerivativeResponse:
    orderNo: str
    pk_orderNo: str
    orderTime: str
    accountCode: str
    side: str
    symbol: str
    volume: int
    showPrice: float
    matchVolume: int
    matchPriceBQ: float
    status: str
    orderStatus: str
    channel: str
    group: str
    cancelTime: str | None
    isCancel: bool
    isAmend: bool
    info: str | None
    maxPrice: float | None
    matchValue: float | None
    quote: str | None
    autoType: str | None
    product: str | None
    orderType: str | None
    source: str | None


@dataclass_json
@dataclass
class ListOrderConditionDerivativeResponse:
    orderNo: str
    groupOrder: str
    pk_orderNo: str
    accountCode: str
    side: str
    symbol: str
    showPrice: float
    volume: int
    condition: str
    result: str
    active_time: str
    send_time: str
    cancel_time: str | None
    group: str
    channel: str
    maxPrice: float | None
    soPrice: float
    orderType: str
    from_time: str
    exp_time: str
    status: str
    details: str
    notes: str


@dataclass_json
@dataclass
class OrderNormalDerivativeResponse:
    symbol: str
    status: str
    msg_type: str
    showPrice: float
    orderTime: str
    type: str
    accountCode: str
    orderNo: str
    matchVolume: float
    side: str
    volume: float
    pk_orderNo: str
    channel: str
    group: str
    quote: str
    accType: str | None = None
    shareStatus: str | None = None
    market: str | None = None
    refID: str | None = None
    autoType: str | None = None
    product: str | None = None


@dataclass
class PlaceOrderDto:
    accountId: str
    subAccountId: str
    side: str
    symbol: str
    price: float
    volume: int
    refId: str
    orderType: str
    advance: int | None = None
    pin: str | None = None


@dataclass
class OrderConditionDerivativeRequestDTO:
    subAccountId: str
    accountId: str
    side: str
    symbol: str
    price: float
    volume: float
    orderType: str
    callbackPoint: float
    activationPrice: float
    soPrice: float
    advance: str | None = None
    refId: str | None = None
    pin: str | None = None
    type: str | None = None
    cmd: str | None = None


@dataclass_json
@dataclass
class OrderConditionDerivativeResponseDTO:
    symbol: str
    status: str
    msg_type: str
    showPrice: float
    orderTime: str
    type: str
    accountCode: str
    orderNo: int
    matchVolume: float
    side: str
    volume: float
    pk_orderNo: str
    channel: str
    group: str
    quote: str
    shareStatus: str | None = None
    market: str | None = None
    refID: str | None = None
    accType: str | None = None
    autoType: str | None = None
    product: str | None = None


@dataclass
class EditOrderNormalDerivativeRequestDTO:
    accountId: str
    subAccountId: str
    orderNo: str
    refId: str
    nvol: float
    nprice: float


@dataclass_json
@dataclass
class EditOrderNormalDerivativeResponseDTO:
    orderNo: str
    msg_type: str
    status: str
    pk_orderNo: str
    volume: float
    showPrice: float


@dataclass
class EditOrderConditionDerivativeRequestDTO:
    accountId: str
    pkOrderNo: str
    type: str
    refId: str
    soPrice: float
    cmd: str | None = None


@dataclass_json
@dataclass
class EditOrderConditionDerivativeResponseDTO:
    showPrice: str
    price: str
    volume: str
    pkOrderNo: str
    notes: str


@dataclass
class CancelOrderNormalDerivativeRequestDTO:
    accountId: str
    orderNo: str
    cmd: str | None = None
    pin: str | None = None
    refId: str | None = None


@dataclass_json
@dataclass
class CancelOrderNormalDerivativeResponseDTO:
    orderNo: str
    msg_type: str | None = None
    status: str | None = None
    pk_orderNo: str | None = None
    cancelTime: str | None = None


@dataclass
class CancelOrderConditionDerivativeRequestDTO:
    accountId: str
    orderNo: str
    subAccountId: str | None = None


@dataclass_json
@dataclass
class CancelOrderConditionDerivativeResponseDTO:
    """Intentionally empty: for this operation TCBS reports only the surrounding envelope."""

    pass


@dataclass
class MarketInformationDerivativeResponseDTO:
    symbol: str | None = None
    ceilPrice: float | None = None
    floorPrice: float | None = None
    refPrice: float | None = None
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
    matchPrice: float | None = None
    matchQtty: float | None = None
    change: float | None = None
    changePercent: float | None = None
    open: float | None = None
    high: float | None = None
    low: float | None = None
    totalVol: float | None = None
    openVol: float | None = None
    buyForeignQtty: float | None = None
    sellForeignQtty: float | None = None
    expiryDate: str | None = None
    avg: float | None = None


@dataclass
class MarketInformationResponseDTO:
    """Price board for every derivatives symbol."""

    data: list[MarketInformationDerivativeResponseDTO]

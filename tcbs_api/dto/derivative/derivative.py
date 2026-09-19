"""Derivatives models, including the envelope every derivative endpoint returns.

``DerivativeResponse[T]`` is that envelope — ``{cmd, rc, rs, oID, data}`` as the document
declares it for every ``/khronos`` call. The payload under ``data`` is modelled only where the
document lists its fields; where it does not, it stays a raw ``dict``. Request bodies carry the
document's properties, with its ``required`` list deciding which have defaults.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from dataclasses_json import dataclass_json

T = TypeVar("T")


@dataclass_json
@dataclass
class DerivativeResponse(Generic[T]):
    """The ``{cmd, rc, rs, oID, data}`` envelope every derivative endpoint returns."""

    cmd: str
    rc: str
    rs: str
    oID: str
    data: T


@dataclass_json
@dataclass
class AssetPositionCloseDerivativeResponse:
    """One closed position (operation 6.2)."""

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
    time: str | None = None


@dataclass_json
@dataclass
class AssetPositionOpenDerivativeResponse:
    """One open position (operation 6.3)."""

    symbol: str
    im: str
    deliver: int
    receive: int
    net: int
    side: str
    lastPrice: float
    imValue: float
    vmValue: float
    mrValue: float
    duedate: str
    pc_remain: str


@dataclass_json
@dataclass
class ListOrderNormalDerivativeResponse:
    """One normal order (operation 6.6)."""

    orderNo: str
    pk_orderNo: str
    side: str
    symbol: str
    volume: float
    showPrice: str
    matchVolume: float
    status: str
    isCancel: str
    isAmend: str


@dataclass_json
@dataclass
class ListOrderConditionDerivativeResponse:
    """One conditional order (operation 6.7)."""

    orderNo: str
    pk_orderNo: str
    side: str
    symbol: str
    showPrice: float
    volume: float
    soPrice: float
    orderType: str
    status: str
    notes: str


@dataclass
class PlaceOrderDto:
    """Body of ``place_order`` (operation 6.4)."""

    accountId: str
    subAccountId: str
    side: str
    symbol: str
    price: float
    volume: int
    orderType: str
    refId: str


@dataclass
class OrderConditionDerivativeRequestDTO:
    """Body of ``place_order_condition`` (operation 6.5)."""

    accountId: str
    subAccountId: str
    side: str
    symbol: str
    price: float
    volume: float
    orderType: str
    soPrice: float
    callbackPoint: float
    activationPrice: float
    refId: str | None = None


@dataclass_json
@dataclass
class OrderNormalDerivativeResponse:
    """One placed order (operation 6.4)."""

    orderNo: str
    pk_orderNo: str
    showPrice: str | None = None


@dataclass_json
@dataclass
class OrderConditionDerivativeResponseDTO:
    """One placed conditional order (operation 6.5)."""

    symbol: str
    status: str
    orderNo: int
    pk_orderNo: str


@dataclass
class EditOrderNormalDerivativeRequestDTO:
    """Body of ``edit_place_order`` (operation 6.8)."""

    accountId: str
    subAccountId: str
    orderNo: str
    refId: str
    nvol: float
    nprice: float


@dataclass_json
@dataclass
class EditOrderNormalDerivativeResponseDTO:
    """Response of ``edit_place_order`` (operation 6.8)."""

    orderNo: str
    status: str
    showPrice: str
    volume: str
    pk_orderNo: str


@dataclass
class EditOrderConditionDerivativeRequestDTO:
    """Body of ``edit_place_order_condition`` (operation 6.9)."""

    accountId: str
    pkOrderNo: str
    refId: str
    soPrice: float
    type: str | None = None
    cmd: str | None = None


@dataclass_json
@dataclass
class EditOrderConditionDerivativeResponseDTO:
    """Response of ``edit_place_order_condition`` (operation 6.9)."""

    showPrice: str
    price: str
    volume: str
    pkOrderNo: str
    notes: str


@dataclass
class CancelOrderNormalDerivativeRequestDTO:
    """Body of ``cancel_place_order`` (operation 6.10)."""

    accountId: str
    orderNo: str
    cmd: str | None = None
    pin: str | None = None
    refId: str | None = None


@dataclass_json
@dataclass
class CancelOrderNormalDerivativeResponseDTO:
    """Response of ``cancel_place_order`` (operation 6.10)."""

    orderNo: str
    status: str
    pk_orderNo: str
    cancelTime: str


@dataclass
class CancelOrderConditionDerivativeRequestDTO:
    """Body of ``cancel_place_order_condition`` (operation 6.11)."""

    accountId: str
    orderNo: str
    subAccountId: str | None = None


@dataclass
class MarketInformationDerivativeResponseDTO:
    """One contract of the derivatives price board (operation 7.1)."""

    symbol: str | None = None
    ceilPrice: float | None = None
    floorPrice: float | None = None
    refPrice: float | None = None
    bidPrice01: float | None = None
    bidQtty01: float | None = None
    offerPrice01: float | None = None
    offerQtty01: float | None = None
    matchPrice: float | None = None
    matchQtty: float | None = None
    change: float | None = None
    changePercent: float | None = None
    totalVol: float | None = None
    openVol: float | None = None
    expiryDate: str | None = None


@dataclass
class MarketInformationResponseDTO:
    """Price board for every derivatives symbol (operation 7.1)."""

    data: list[MarketInformationDerivativeResponseDTO]

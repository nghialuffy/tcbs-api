"""Stock order, purchasing-power, asset and cash models.

Every field is one the TCBS OpenAPI document declares for the operation that returns it, the
``*Dto``/``*RequestDto`` classes are request bodies, and models are named after their
operation. The typing and optionality rules shared by every model live in
:mod:`tcbs_api.dto`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlaceOrderExternalDto:
    execType: str
    price: int
    priceType: str
    quantity: int
    symbol: str


@dataclass
class PlaceOrderResponse:
    """Response of ``place_order`` (operation 4.1)."""

    error: str
    message: str
    orderId: str


@dataclass
class UpdateOrderRequestDto:
    price: int
    quantity: int


@dataclass
class UpdateOrderResponse:
    """Response of ``update_order`` (operation 4.2)."""

    error: str
    message: str
    orderId: str


@dataclass
class OrderIDResponse:
    orderID: str


@dataclass
class CancelOrderRequestDto:
    ordersList: list[OrderIDResponse]


@dataclass
class CancelOrderResponse:
    """Response of ``cancel_order`` (operation 4.3) — per-order outcomes are not reported."""

    error: str
    message: str


@dataclass
class OrderSummary:
    """One order of the order book returned by ``get_orders`` (operation 4.4)."""

    orderId: str
    symbol: str
    execType: str
    price: int
    quantity: int
    status: str


@dataclass
class OrderSearchResponse:
    """Response of ``get_orders`` (operation 4.4)."""

    orders: list[OrderSummary] | None = None


@dataclass
class OrderDetail:
    """One order as returned by ``get_order`` (operation 4.5)."""

    orderID: str
    accountNo: str
    symbol: str
    execType: str
    orderQtty: float
    execQtty: float
    priceType: str
    limitPrice: float
    matchPrice: float
    orStatus: str
    txdate: str
    txtime: str


@dataclass
class OrderDetailResponse:
    """Response of ``get_order`` (operation 4.5)."""

    object: str
    pageSize: int
    pageIndex: int
    totalCount: int
    data: list[OrderDetail] | None = None


@dataclass
class CommandMatchInformationDetailResponse:
    """One trade match of ``get_command_match_information`` (operation 4.6)."""

    orderId: str
    side: str
    symbol: str
    quoteQtty: float
    quotePrice: float
    tradeId: str
    qtty: float
    price: float
    timeExec: str


@dataclass
class CommandMatchInformationResponse:
    """Response of ``get_command_match_information`` (operation 4.6)."""

    totalCount: int
    pageSize: int
    pageIndex: int
    data: list[CommandMatchInformationDetailResponse] | None = None


@dataclass
class PurchasingPowerResponse:
    """Response of ``get_purchasing_power`` (operation 4.7)."""

    purchasingPower: float = 0.0
    maxQuantity: int = 0


@dataclass
class PurchasingPowerBySymbolResponse:
    """Response of the by-symbol purchasing-power endpoints (operations 4.8 and 4.9)."""

    pp0: float
    maxQtty: float


@dataclass
class StockAsset:
    """One stock holding of a sub-account, as returned by ``get_asset_stock_by_sub_account``."""

    symbol: str
    quantity: int
    avgPrice: float
    marketValue: float


@dataclass
class StockAssetResponse:
    """Response of ``get_asset_stock_by_sub_account`` (operation 4.14)."""

    assets: list[StockAsset] | None = None


@dataclass
class CashInvestmentInfo:
    """One cash-balance record of ``get_cash_investment`` (operation 4.15)."""

    bodBalance: float
    cashBalance: float
    pp0forBF: float
    bankAvlBalanceBF: float
    accountNo: str


@dataclass
class CashInvestmentResponse:
    """Response of ``get_cash_investment`` (operation 4.15)."""

    totalCount: int
    pageSize: int
    pageIndex: int
    data: list[CashInvestmentInfo] | None = None


@dataclass
class CashStatementDetail:
    """One line of a sub-account's cash statement."""

    custodyID: str
    transactionCode: str
    transactionName: str
    debitAmount: float
    creditAmount: float
    businessDate: str
    transactionDate: str
    descriptions: str


@dataclass
class CashStatementPage:
    """The page of statement lines, with its own totals."""

    pageIndex: int
    pageSize: int
    totalCreditAmount: int
    totalDebitAmount: int
    totalCount: int
    data: list[CashStatementDetail] | None = None


@dataclass
class CashStatementResponse:
    """Response of ``get_cash_statement`` (operation 4.16) — TCBS nests the page one level down."""

    response: CashStatementPage

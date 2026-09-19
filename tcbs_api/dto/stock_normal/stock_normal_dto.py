"""Stock order, purchasing-power, holding and cash models.

The ``*Dto``/``*RequestDto`` models are request bodies. The rest are responses; ``OrderInfo``
is the full order-book record and the largest model in the library, and ``Response`` is the
purchasing-power record shared by the three ``ppse`` endpoints.
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
    orderId: str
    error: str
    message: str


@dataclass
class UpdateOrderRequestDto:
    price: int
    quantity: int


@dataclass
class UpdateOrderResponse:
    orderId: str
    error: str
    message: str


@dataclass
class OrderIDResponse:
    orderID: str


@dataclass
class CancelOrderRequestDto:
    ordersList: list[OrderIDResponse]


@dataclass
class Detail:
    """The outcome for a single order inside a cancel-order response."""

    deleted: str
    errorCode: str
    errorMesage: str
    orderID: str


@dataclass
class DataX:
    """Groups the per-order outcomes reported for one cancel request."""

    details: list[Detail]
    object: str


@dataclass
class CancelOrderResponse:
    """Response of ``cancel_order`` — check each entry in ``data`` for per-order success."""

    data: list[DataX]
    object: str
    pageIndex: int
    pageSize: int
    totalCount: int


@dataclass
class OrderInfo:
    """One row of the order book — the full record TCBS keeps for an order."""

    object: str
    accountNo: str
    orderID: str
    execType: str
    orderQtty: float
    execQtty: float
    codeID: str
    symbol: str
    priceType: str
    txtime: str
    txdate: str
    expDate: str
    timeType: str
    orStatus: str
    feeAcr: float
    limitPrice: float
    cancelQtty: float
    remainQtty: float
    via: str
    quotePrice: float
    matchPrice: float
    tradePlace: str
    matchType: str
    isDisposal: str
    isCancel: str
    isAmend: str
    userName: str
    orsOrderID: str
    sectype: str
    isFOOrder: str
    odTimeStamp: str
    matchAmount: float
    mmType: str
    bRatio: float
    taxSellAmout: float


@dataclass
class OrderSearchResponse:
    object: str
    pageSize: int
    pageIndex: int
    totalCount: int
    data: list[OrderInfo] | None = None


@dataclass
class CommandMatchInformationDetailResponse:
    orderId: str
    side: str
    symbol: str
    quoteQtty: int
    quotePrice: float
    tradeId: str
    qtty: int
    price: float
    timeExec: str


@dataclass
class CommandMatchInformationResponse:
    object: str
    totalCount: int
    pageSize: int
    pageIndex: int
    data: list[CommandMatchInformationDetailResponse] | None = None


@dataclass
class Response:
    """The purchasing-power record shared by the three ``ppse`` endpoints."""

    accountNo: str
    symbol: str
    price: float
    pp0: float
    ppse: float
    ppseref: float
    maxBuyQuantity: float
    realMaxBuyQuantity: float
    minBuyQuantity: float
    marginRatioLoan: str
    marginPriceLoan: str
    rateBrkS: float
    rateBrkB: float
    custodyID: str | None = None


@dataclass
class StockHoldingInfo:
    """Per-symbol holding breakdown: free, mortgaged, pending and settlement quantities."""

    symbol: str
    secType: str
    secTypeName: str | None
    availableTrading: float
    mortgaged: float
    t0: float
    t1: float
    t2: float
    blocked: float
    securedQuantity: float
    sellRemain: float
    exercisedCA: float
    unexercisedCA: float
    stockDividend: float
    cashDividend: float
    waitForTrade: float
    waitForTransfer: float
    waitForWithdraw: float
    currentPrice: float
    costPrice: float
    sellExec: float
    totalQtty: float
    settlement: float


@dataclass
class SeInfoDTO:
    """Stock holdings of a sub-account: one ``StockHoldingInfo`` per symbol."""

    object: str
    accountNo: str
    custodyID: str
    fullName: str
    stock: list[StockHoldingInfo]


@dataclass
class IAInfo:
    """One partner's balance within ``CashInvestmentInfo.iaInfos``."""

    partner: str
    available: float
    hold: float


@dataclass
class CashInvestmentInfo:
    """Cash balance and buying power of a sub-account."""

    object: str
    iaInfos: list[IAInfo]
    pp0forBF: float
    bankAvlBalanceBF: float
    bodBalance: float
    cashBalance: float
    accountNo: str
    custodyID: str
    fullName: str
    balance: float
    avlAdvanceAmount: float
    buyingAmount: float
    blockAmount: float
    cashDevident: float
    bankAvlBalance: float
    bankBlockAmount: float
    avlWithdraw: float
    pp0: float
    secureAmtPO: float
    bondBlockAmount: float
    mBlockAmount: float
    fundBlockAmount: float
    avalBondBlockAmount: float
    depoFee: float
    bCashDividend: float
    sCashDividend: float
    dsecured: float
    adused: float
    mrused: float


@dataclass
class CashInvestmentResponse:
    object: str
    totalCount: int
    pageSize: int
    pageIndex: int
    data: list[CashInvestmentInfo]


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
    data: list[CashStatementDetail]


@dataclass
class CashStatementResponse:
    """Response of ``get_cash_statement`` — TCBS nests the page one level down."""

    response: CashStatementPage

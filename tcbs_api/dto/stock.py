"""Stock order, purchasing-power, asset and cash models.

Every field is one the TCBS OpenAPI document declares for the operation that returns it, and
models are named after their operation. The typing and optionality rules shared by every model
live in `tcbs_api.dto`.

``StockAsset`` (4.14) and ``CashInvestmentInfo`` (4.15) are the exceptions: the document
describes those responses thinly or wrongly — 4.14 as ``assets`` records of four fields, 4.15
as five of its thirty — so those models follow real payloads instead.
"""

from __future__ import annotations

from pydantic import Field

from tcbs_api.dto.base import DtoModel


class OrderSummary(DtoModel):
    """One order of the order book returned by ``get_orders`` (operation 4.4)."""

    orderId: str = Field(description="Order ID.")
    symbol: str = Field(description="Stock symbol.")
    execType: str = Field(description="Trading direction (NB/NS).")
    price: int = Field(description="Order price.")
    quantity: int = Field(description="Order quantity.")
    status: str = Field(description="Order status.")


class OrderSearchResponse(DtoModel):
    """Response of ``get_orders`` (operation 4.4) — a page of the order book.

    The document calls the rows ``orders``; the endpoint sends them under ``data``, beside the
    ``object``/``totalCount``/``pageSize``/``pageIndex`` header the other paged responses carry.
    """

    object: str | None = Field(default=None, description="Envelope object name, list.")
    totalCount: int | None = Field(default=None, description="Total number of records.")
    pageSize: int | None = Field(default=None, description="Page size.")
    pageIndex: int | None = Field(default=None, description="Page index.")
    data: list[OrderSummary] | None = Field(
        default=None,
        description="The orders on this page; the document calls this key orders.",
    )


class OrderDetail(DtoModel):
    """One order as returned by ``get_order`` (operation 4.5)."""

    orderID: str = Field(description="Order ID.")
    accountNo: str = Field(description="Account number.")
    symbol: str = Field(description="Stock symbol.")
    execType: str = Field(description="Order type (NB/NS).")
    orderQtty: float = Field(description="Order quantity.")
    execQtty: float = Field(description="Matched quantity.")
    priceType: str = Field(description="Price type.")
    limitPrice: float = Field(description="Order price.")
    matchPrice: float = Field(description="Average match price.")
    orStatus: str = Field(
        description=(
            "Order status: 0 = Rejected, 2 = Sent, 3 = Canceled, 4 = Matched, 5 = Expired, "
            "8 = Waiting, 10 = Modified, 11 = Sending, 12 = Matched all, A = Modifying, "
            "C = Canceling, S = Completed."
        ),
    )
    txdate: str = Field(description="Order date (RFC 3339).")
    txtime: str = Field(description="Order time.")


class OrderDetailResponse(DtoModel):
    """Response of ``get_order`` (operation 4.5)."""

    object: str = Field(description="Envelope object name, list.")
    pageSize: int = Field(description="Page size.")
    pageIndex: int = Field(description="Page index.")
    totalCount: int = Field(description="Total number of records.")
    data: list[OrderDetail] | None = Field(default=None, description="The orders on this page.")


class CommandMatchInformationDetailResponse(DtoModel):
    """One trade match of ``get_command_match_information`` (operation 4.6)."""

    orderId: str = Field(description="Order ID.")
    side: str = Field(description="Direction: S = Sell, B = Buy.")
    symbol: str = Field(description="Stock symbol.")
    quoteQtty: float = Field(description="Order volume.")
    quotePrice: float = Field(description="Bid price.")
    tradeId: str = Field(description="Match trade ID.")
    qtty: float = Field(description="Matched volume.")
    price: float = Field(description="Matching price.")
    timeExec: str = Field(description="Matching time.")


class CommandMatchInformationResponse(DtoModel):
    """Response of ``get_command_match_information`` (operation 4.6)."""

    object: str | None = Field(default=None, description="Envelope object name, list.")
    totalCount: int = Field(description="Total number of records returned.")
    pageSize: int = Field(description="Number of elements per page.")
    pageIndex: int = Field(description="Page index.")
    data: list[CommandMatchInformationDetailResponse] | None = Field(
        default=None,
        description="The matches on this page.",
    )


class PurchasingPowerResponse(DtoModel):
    """Response of the 4.7, 4.8 and 4.9 purchasing-power endpoints.

    All three return the same payload — the ``ppse`` object below — even though the document
    describes 4.7 as a bare ``purchasingPower``/``maxQuantity`` pair and 4.8/4.9 as
    ``pp0``/``maxQtty``. The field set is the live one; every field is optional because the
    endpoint omits the ones that do not apply (a symbol with no bracket, a null ``custodyID``).

    ``pp0`` is spendable **cash**, not leverage. It gathers every cash layer the account really
    holds — cash at TCBS, cash at the IA partner and pending receivables — so it can be larger
    than 4.15's cash figure with no margin in use. Never infer a loan from ``pp0`` > cash.

    ``minBuyQuantity`` is **not** the exchange's round-lot rule. On HOSE a lot is 100 shares, and
    this value does not change with price, so no lot size can be read out of it; TCBS documents
    neither it nor ``availableTrade``/``ppseref``/``realMaxBuyQuantity`` at all.
    """

    object: str | None = Field(default=None, description="Envelope object name, ppse.")
    rateBrkS: float | None = Field(default=None, description="Brokerage rate for the selling side.")
    rateBrkB: float | None = Field(default=None, description="Brokerage rate for the buying side.")
    accountNo: str | None = Field(default=None, description="Account number.")
    custodyID: str | None = Field(default=None, description="Custody ID.")
    symbol: str | None = Field(default=None, description="Stock symbol.")
    price: float | None = Field(default=None, description="Price the check was run at.")
    pp0: float | None = Field(default=None, description="Basic purchasing power: spendable cash, not leverage.")
    ppse: float | None = Field(default=None, description="Purchasing power for this symbol at this price.")
    availableTrade: float | None = Field(default=None, description="Not documented by TCBS; cash available to trade.")
    ppseref: float | None = Field(default=None, description="Not documented by TCBS; a reference purchasing power.")
    maxBuyQuantity: float | None = Field(default=None, description="Maximum buyable quantity — document's maxQtty.")
    realMaxBuyQuantity: float | None = Field(default=None, description="Undocumented; larger max than maxBuyQuantity.")
    minBuyQuantity: float | None = Field(
        default=None,
        description="Not documented by TCBS, and not a lot rule — a HOSE round lot is 100 shares.",
    )
    marginRatioLoan: str | None = Field(
        default=None,
        description="Margin ratio applied to the loan — a string in the payload.",
    )
    marginPriceLoan: str | None = Field(default=None, description="Margin price of the loan — a string in the payload.")


class StockAsset(DtoModel):
    """One stock holding of a sub-account, as returned by ``get_asset_stock_by_sub_account``.

    Quantities are whole shares, prices are VND, and ``t0``/``t1``/``t2`` are the shares that
    become tradable today, tomorrow and the day after. ``secTypeName`` is the only field the
    API returns as null.
    """

    symbol: str = Field(description="Stock symbol.")
    secType: str = Field(description="Security type code, e.g. 001 for a stock, 008 for an ETF.")
    availableTrading: int = Field(description="Shares that can be sold today.")
    availableTradingForBuyIn: int = Field(description="Shares that can be bought back today (buy-in).")
    mortgaged: int = Field(description="Shares pledged as collateral.")
    t0: int = Field(description="Shares bought today, still to settle.")
    t1: int = Field(description="Shares bought yesterday, settling tomorrow.")
    t2: int = Field(description="Shares bought two days ago, settling today.")
    blocked: int = Field(description="Shares blocked from trading.")
    securedQuantity: int = Field(description="Shares pledged against a loan.")
    sellRemain: int = Field(description="Shares still to be sold.")
    exercisedCA: int = Field(description="Corporate-action shares already exercised.")
    unexercisedCA: int = Field(description="Corporate-action shares not yet exercised.")
    stockDividend: int = Field(description="Shares pending from a stock dividend.")
    cashDividend: int = Field(description="Cash dividend pending.")
    waitForTrade: int = Field(description="Shares waiting to become tradable.")
    waitForTransfer: int = Field(description="Shares waiting to be transferred.")
    waitForWithdraw: int = Field(description="Shares waiting to be withdrawn.")
    currentPrice: float = Field(description="Current market price.")
    costPrice: float = Field(description="Average cost of the holding.")
    sellExec: int = Field(description="Shares already sold today.")
    sbType: str = Field(description="Sub-type within secType.")
    onHold: int = Field(description="Shares on hold.")
    settlement: str = Field(description="Settlement cycle, e.g. DVP3.")
    rt2_selling: str = Field(description="Whether shares can be sold before settlement (Y/N).")
    totalQtty: int = Field(description="Total quantity held.")
    receiving_selling: str = Field(description="Shares being received that are also being sold.")
    holdQtty: int = Field(description="Quantity on hold.")
    buyingQtty: int | None = Field(default=None, description="Shares in a pending buy. Not documented by TCBS.")
    tradeQtty: int | None = Field(
        default=None,
        description="Shares that have settled and are tradable. Not documented by TCBS.",
    )
    sellReceivingQtty: int | None = Field(
        default=None,
        description="Shares sold but not yet received. Not documented by TCBS.",
    )
    secTypeName: str | None = Field(default=None, description="Security type name — null in every sampled row.")


class StockAssetResponse(DtoModel):
    """Response of ``get_asset_stock_by_sub_account`` (operation 4.14)."""

    object: str = Field(description="Envelope object name, se.")
    accountNo: str = Field(description="Sub-account number.")
    custodyID: str = Field(description="Custody account number.")
    fullName: str = Field(description="Account holder name.")
    stock: list[StockAsset] | None = Field(default=None, description="One row per stock held.")


class CashInvestmentIaInfo(DtoModel):
    """One IA partner's balance inside a ``CashInvestmentInfo``.

    ``available`` is the cash the partner can still use and ``hold`` the part already
    committed.
    """

    partner: str = Field(description="IA partner code, e.g. TCB.")
    status: str = Field(description="Whether the partner link is active (Y/N).")
    available: float = Field(description="Cash the partner can still use — real money, counted in pp0.")
    hold: float = Field(description="Cash already committed at the partner.")


class CashInvestmentBlockAmountDetail(DtoModel):
    """One blocked-amount line, by reason."""

    blockType: str = Field(description="Why the cash is blocked, e.g. SE_TRANSF, IPO_OFFICIAL, OTHER.")
    blockAmt: float = Field(description="Amount blocked for that reason.")


class CashInvestmentBlockAmountInfo(DtoModel):
    """The ``blockAmountInfo`` block of a ``CashInvestmentInfo``."""

    blockAmountTotal: float = Field(description="Total blocked across every reason.")
    details: list[CashInvestmentBlockAmountDetail] | None = Field(
        default=None,
        description="One line per blocking reason.",
    )


class CashInvestmentInfo(DtoModel):
    """One cash-balance record of ``get_cash_investment`` (operation 4.15).

    TCBS spreads the money over four layers. Read them apart — do not add them into one number:

    * **Cash at TCBS** — ``bodBalance``, with ``cashBalance`` as the document's twin of it. This
      is the money actually sitting in the sub-account.
    * **Cash at the IA partner** — ``bankAvlBalance`` and each ``iaInfos[].available``. Real money
      held at the partner (e.g. TCB), a layer of its own and not a loan.
    * **In transit** — ``balance``, a field the API document does not declare. It can be
      **negative**, and a negative value means money still moving — unsettled sells and pending
      settlements — not an overdraft. It is not available cash.
    * **Committed** — ``buyingAmount``, ``secureAmtPO``, ``blockAmount`` and the ``*BlockAmount``
      counters: cash earmarked for pending orders, still the account's money but not free.

    ``pp0`` is what can actually be spent across those layers. It is **not** a margin or leverage
    figure, so ``pp0`` above ``bodBalance`` does not mean a loan is in use.

    Field names keep the API's spelling, including its ``pp0forBF``/``pp0ForBond`` capitalisation
    split and the ``cashDevident``/``avalBondBlockAmount`` typos; ``fullName`` comes back as the
    four-character string ``"null"`` rather than JSON null.
    """

    object: str = Field(description="Envelope object name, cashInvestment.")
    pp0forBF: float = Field(description="Basic purchasing power for BOND/FUND — spendable cash, not leverage.")
    pp0ForBond: float = Field(description="Basic purchasing power for bonds; mirrors pp0forBF in every sample.")
    bankAvlBalanceBF: float = Field(description="IA-partner cash available for BOND/FUND products.")
    bodBalance: float = Field(description="Cash at TCBS — the money actually in the sub-account.")
    cashBalance: float = Field(description="Cash at TCBS; the document calls it simply 'tiền mặt'.")
    stockBlockAmount: float = Field(description="Cash blocked for stock orders.")
    dsecured: float = Field(description="Not documented by TCBS; 0 in the sampled record.")
    accountNo: str = Field(description="Account number.")
    custodyID: str = Field(description="Custody account number.")
    fullName: str = Field(description='Holder name — the four-character string "null" in the sampled payload.')
    balance: float = Field(
        description="In-transit; not in the document. Negative means unsettled, not an overdraft, not spendable cash.",
    )
    avlAdvanceAmount: float = Field(description="Advance amount already used. Not documented by TCBS.")
    buyingAmount: float = Field(description="Cash committed to pending buy orders — earmarked, still the account's.")
    blockAmount: float = Field(description="Total cash blocked.")
    cashDevident: float = Field(description="Cash dividend pending (TCBS's spelling).")
    bankAvlBalance: float = Field(description="Cash held at the IA partner — a real-money layer of its own.")
    bankBlockAmount: float = Field(description="Cash blocked at the IA partner.")
    avlWithdraw: float = Field(description="Cash available to withdraw.")
    pp0: float = Field(description="Basic purchasing power: spendable cash, not leverage.")
    secureAmtPO: float = Field(description="Cash secured for pending orders.")
    bondBlockAmount: float = Field(description="Cash blocked for bond orders.")
    fundBlockAmount: float = Field(description="Cash blocked for fund orders.")
    avalBondBlockAmount: float = Field(
        description="Balance available for bonds once blocking is applied (TCBS's spelling).",
    )
    depoFee: float = Field(description="Depositary fee.")
    bCashDividend: float = Field(description="Cash dividend from buy-side trades.")
    sCashDividend: float = Field(description="Cash dividend from sell-side trades.")
    adused: float = Field(description="Not documented by TCBS; 0 in the sampled record.")
    mrused: float = Field(description="Not documented by TCBS; 0 in the sampled record.")
    mBlockAmount: float = Field(description="Cash blocked for margin.")
    iaInfos: list[CashInvestmentIaInfo] | None = Field(default=None, description="Balances held at each IA partner.")
    blockAmountInfo: CashInvestmentBlockAmountInfo | None = Field(default=None, description="What is blocked, and why.")


class CashInvestmentResponse(DtoModel):
    """Response of ``get_cash_investment`` (operation 4.15)."""

    object: str = Field(description="Envelope object name, list.")
    totalCount: int = Field(description="Total number of records.")
    pageSize: int = Field(description="Page size (default = 20).")
    pageIndex: int = Field(description="Page index (default = 1).")
    data: list[CashInvestmentInfo] | None = Field(default=None, description="One record per sub-account.")


class CashStatementDetail(DtoModel):
    """One line of a sub-account's cash statement.

    ``transactionDate`` carries the wire key ``transationDate`` — TCBS's spelling, missing the
    second ``c`` — as an alias, so the field keeps a readable name and still decodes.
    """

    custodyID: str = Field(description="Custody ID.")
    transactionCode: str = Field(description="Transaction code.")
    transactionName: str = Field(description="Transaction name.")
    debitAmount: float = Field(description="Debit amount.")
    creditAmount: float = Field(description="Credit amount.")
    businessDate: str = Field(description="Business date.")
    transactionDate: str = Field(alias="transationDate", description="Transaction date — wire key transationDate.")
    descriptions: str = Field(description="Description.")
    transactionNum: str | None = Field(default=None, description="Transaction number.")
    accountNo: str | None = Field(default=None, description="Account number.")


class CashStatementPage(DtoModel):
    """The page of statement lines, with its own totals.

    The endpoint answers ``{"response": {"data": []}}`` when there is nothing to report — no
    ``pageIndex``, no totals — so every scalar here is optional.
    """

    pageIndex: int | None = Field(default=None, description="Page index.")
    pageSize: int | None = Field(default=None, description="Page size.")
    totalCreditAmount: int | None = Field(default=None, description="Total credit amount.")
    totalDebitAmount: int | None = Field(default=None, description="Total debit amount.")
    totalCount: int | None = Field(default=None, description="Total records.")
    data: list[CashStatementDetail] | None = Field(default=None, description="The statement lines on this page.")


class CashStatementResponse(DtoModel):
    """Response of ``get_cash_statement`` (operation 4.16) — TCBS nests the page one level down."""

    response: CashStatementPage = Field(description="The page of statement lines, nested one level down.")

"""Stock (normal) trading: order and trade lookup, purchasing power, assets and cash.

Every function here is a thin declaration of one endpoint — the URL, the verb and the
response DTO. The request plumbing lives in `tcbs_api.utils.request_api`.
"""

from __future__ import annotations

from tcbs_api.dto import stock
from tcbs_api.utils import request_api


def get_orders(account_no: str, token: str) -> stock.OrderSearchResponse:
    """Get the order book of a sub-account.

    Operation 4.4 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/get-orders/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/orders", token)
    return request_api.decode(stock.OrderSearchResponse, payload)


def get_order(account_no: str, order_id: str, token: str) -> stock.OrderDetailResponse:
    """Get a single order from the order book.

    Operation 4.5 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/get-order-by-id/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/orders/{order_id}", token)
    return request_api.decode(stock.OrderDetailResponse, payload)


def get_command_match_information(account_no: str, token: str) -> stock.CommandMatchInformationResponse:
    """Get the trade-matching details of a sub-account.

    Operation 4.6 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/matching-details/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/matching-details", token)
    return request_api.decode(stock.CommandMatchInformationResponse, payload)


def get_purchasing_power(account_no: str, token: str) -> stock.PurchasingPowerResponse:
    """Get the purchasing power of a sub-account.

    Operation 4.7 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/purchasing-power/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/ppse", token)
    return request_api.decode(stock.PurchasingPowerResponse, payload)


def get_purchasing_power_by_symbol(
    account_no: str,
    symbol: str,
    token: str,
) -> stock.PurchasingPowerResponse:
    """Get the purchasing power of a sub-account for one symbol.

    Operation 4.8 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/purchasing-power-symbol/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/ppse/{symbol}", token)
    return request_api.decode(stock.PurchasingPowerResponse, payload)


def get_purchasing_power_by_symbol_and_price(
    account_no: str,
    symbol: str,
    price: float,
    token: str,
) -> stock.PurchasingPowerResponse:
    """Get the purchasing power of a sub-account for a symbol at a given price.

    Operation 4.9 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/purchasing-power-symbol-price/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/ppse/{symbol}/{price}", token)
    return request_api.decode(stock.PurchasingPowerResponse, payload)


def get_asset_stock_by_sub_account(account_no: str, token: str) -> stock.StockAssetResponse:
    """Get the stock assets held by a sub-account.

    Operation 4.14 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/asset/

    Each holding in ``stock`` reports what can be sold now (``availableTrading``), what is
    still settling (``t0``/``t1``/``t2``) and the dividends pending.
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/se", token)
    return request_api.decode(stock.StockAssetResponse, payload)


def get_cash_investment(account_no: str, token: str) -> stock.CashInvestmentResponse:
    """Get the cash balance and remaining buying power of a sub-account.

    Operation 4.15 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/cash-balance/

    A record's ``balance`` is the cash at TCBS, ``pp0`` what can be bought with today, and
    ``blockAmountInfo`` breaks down what is blocked and why; ``iaInfos`` carries the same
    figures per IA partner.
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/cashInvestments", token)
    return request_api.decode(stock.CashInvestmentResponse, payload)


def get_cash_statement(
    account_no: str,
    from_date: str,
    to_date: str,
    transaction_code: str,
    token: str,
    page_size: int = 10,
    page_index: int = 0,
) -> stock.CashStatementResponse:
    """Get the cash statement — the transaction history — of a sub-account.

    Operation 4.16 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/cash-statement/

    `account_no` is the sub-account number and `from_date`/`to_date` are ``YYYY-MM-DD``
    strings. All six query parameters are required by TCBS, including `transaction_code` — an
    empty one is rejected — and the documented sample uses ``1153`` ("ứng trước tiền bán").
    ``page_index`` is 1-based in that sample. The sub-account goes in `acctno`: the document
    calls that parameter ``accountno``, but the endpoint does not answer to it.
    """
    payload = request_api.get(
        "/erebos/v2/digital/trans-hist-cashStatements",
        token,
        params={
            "acctno": account_no,
            "fromDate": from_date,
            "toDate": to_date,
            "pageSize": page_size,
            "pageIndex": page_index,
            "transactionCode": transaction_code,
        },
    )
    return request_api.decode(stock.CashStatementResponse, payload)

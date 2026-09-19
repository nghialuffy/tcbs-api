"""Stock (normal) trading: order lifecycle, purchasing power, assets and cash.

Every function here is a thin declaration of one endpoint — the URL, the verb and the
response DTO. The request plumbing lives in :mod:`tcbs_api.utils.request_api`.
"""

from __future__ import annotations

from dataclasses import asdict

from tcbs_api.dto.stock_normal import stock_normal
from tcbs_api.utils import request_api


def place_order(
    request_dto: stock_normal.PlaceOrderExternalDto,
    account_no: str,
    token: str,
) -> stock_normal.PlaceOrderResponse:
    """Place a normal stock order.

    Operation 4.1 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/place-order/
    """
    payload = request_api.post(f"/akhlys/v1/accounts/{account_no}/orders", token, body=asdict(request_dto))
    return request_api.decode(stock_normal.PlaceOrderResponse, payload)


def update_order(
    request_dto: stock_normal.UpdateOrderRequestDto,
    account_no: str,
    order_id: str,
    token: str,
) -> stock_normal.UpdateOrderResponse:
    """Amend the price or quantity of a working order.

    Operation 4.2 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/update-order/
    """
    payload = request_api.put(f"/akhlys/v1/accounts/{account_no}/orders/{order_id}", token, body=asdict(request_dto))
    return request_api.decode(stock_normal.UpdateOrderResponse, payload)


def cancel_order(
    account_no: str,
    request_dto: stock_normal.CancelOrderRequestDto,
    token: str,
) -> stock_normal.CancelOrderResponse:
    """Cancel one or more working orders.

    Operation 4.3 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/cancel-order/

    The response reports per-order success, so check each entry in ``data`` rather than
    treating a 200 as "all cancelled".
    """
    payload = request_api.put(f"/akhlys/v1/accounts/{account_no}/cancel-orders", token, body=asdict(request_dto))
    return request_api.decode(stock_normal.CancelOrderResponse, payload)


def get_orders(account_no: str, token: str) -> stock_normal.OrderSearchResponse:
    """Get the order book of a sub-account.

    Operation 4.4 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/get-orders/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/orders", token)
    return request_api.decode(stock_normal.OrderSearchResponse, payload)


def get_order(account_no: str, order_id: str, token: str) -> stock_normal.OrderDetailResponse:
    """Get a single order from the order book.

    Operation 4.5 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/get-order-by-id/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/orders/{order_id}", token)
    return request_api.decode(stock_normal.OrderDetailResponse, payload)


def get_command_match_information(account_no: str, token: str) -> stock_normal.CommandMatchInformationResponse:
    """Get the trade-matching details of a sub-account.

    Operation 4.6 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/matching-details/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/matching-details", token)
    return request_api.decode(stock_normal.CommandMatchInformationResponse, payload)


def get_purchasing_power(account_no: str, token: str) -> stock_normal.PurchasingPowerResponse:
    """Get the purchasing power of a sub-account.

    Operation 4.7 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/purchasing-power/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/ppse", token)
    return request_api.decode(stock_normal.PurchasingPowerResponse, payload)


def get_purchasing_power_by_symbol(
    account_no: str,
    symbol: str,
    token: str,
) -> stock_normal.PurchasingPowerBySymbolResponse:
    """Get the purchasing power of a sub-account for one symbol.

    Operation 4.8 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/purchasing-power-symbol/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/ppse/{symbol}", token)
    return request_api.decode(stock_normal.PurchasingPowerBySymbolResponse, payload)


def get_purchasing_power_by_symbol_and_price(
    account_no: str,
    symbol: str,
    price: float,
    token: str,
) -> stock_normal.PurchasingPowerBySymbolResponse:
    """Get the purchasing power of a sub-account for a symbol at a given price.

    Operation 4.9 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/purchasing-power-symbol-price/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/ppse/{symbol}/{price}", token)
    return request_api.decode(stock_normal.PurchasingPowerBySymbolResponse, payload)


def get_asset_stock_by_sub_account(account_no: str, token: str) -> stock_normal.StockAssetResponse:
    """Get the stock assets held by a sub-account.

    Operation 4.14 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/asset/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/se", token)
    return request_api.decode(stock_normal.StockAssetResponse, payload)


def get_cash_investment(account_no: str, token: str) -> stock_normal.CashInvestmentResponse:
    """Get the cash balance and remaining buying power of a sub-account.

    Operation 4.15 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/cash-balance/
    """
    payload = request_api.get(f"/aion/v1/accounts/{account_no}/cashInvestments", token)
    return request_api.decode(stock_normal.CashInvestmentResponse, payload)


def get_cash_statement(
    account_no: str,
    from_date: str,
    to_date: str,
    page_size: int,
    page_index: int,
    transaction_code: str,
    token: str,
) -> stock_normal.CashStatementResponse:
    """Get the cash statement — the transaction history — of a sub-account.

    Operation 4.16 — https://developers.tcbs.com.vn/docs/v1.0.0/stock/cash-statement/

    `account_no` is the sub-account number and `from_date`/`to_date` are ``YYYY-MM-DD``
    strings. `transaction_code` narrows the statement to one transaction type; TCBS
    documents the parameter but not the codes it accepts.
    """
    payload = request_api.get(
        "/erebos/v2/digital/trans-hist-cashStatements",
        token,
        params={
            "accountno": account_no,
            "fromDate": from_date,
            "toDate": to_date,
            "pageSize": page_size,
            "pageIndex": page_index,
            "transactionCode": transaction_code,
        },
    )
    return request_api.decode(stock_normal.CashStatementResponse, payload)

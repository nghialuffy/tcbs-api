"""Derivatives trading: cash and margin, positions, order lifecycle and market data.

These endpoints answer with a ``{cmd, rc, rs, oID, data}`` envelope rather than a bare
object, and their payloads are decoded with ``dataclasses_json`` instead of ``dacite``.
Both differences are handled by :func:`_envelope`.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, TypeVar

from tcbs_api.dto.derivative_dto import derivative_dto
from tcbs_api.utils import request_api

T = TypeVar("T")


def _envelope(data_class: type[T], payload: Any) -> derivative_dto.DerivativeResponse[T]:
    """Unwrap one ``{cmd, rc, rs, oID, data}`` envelope into its declared DTO.

    Note that the envelope's ``data`` is left as a raw ``dict``: ``dataclasses_json``
    cannot resolve the ``Generic[T]`` parameter, so the declared element type is not
    applied. Decode it yourself if you need the typed object::

        data_class.from_dict(envelope.data, infer_missing=True)
    """
    return derivative_dto.DerivativeResponse[data_class].from_json(json.dumps(payload))


def get_total_cash_derivative(
    account_id: str,
    sub_account_id: str,
    get_type: str,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.TotalCashDerivativeResponse]:
    """Get the derivatives cash, margin and collateral summary.

    Operation 6.1 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/account-status/
    """
    payload = request_api.get(
        "/khronos/v1/account/status",
        token,
        params={"accountId": account_id, "subAccountId": sub_account_id, "getType": get_type},
    )
    return _envelope(derivative_dto.TotalCashDerivativeResponse, payload)


def get_asset_position_close(
    account_id: str,
    sub_account_id: str,
    symbol: str | None,
    page_no: int,
    page_size: int,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.AssetPositionCloseDerivativeResponse]:
    """Get closed derivatives positions.

    Operation 6.2 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/position-closed/

    Pass ``None`` for `symbol` to return every symbol.
    """
    payload = request_api.get(
        "/khronos/v1/account/portfolio/position/close",
        token,
        params={
            "accountId": account_id,
            "subAccountId": sub_account_id,
            "symbol": symbol,
            "pageNo": page_no,
            "pageSize": page_size,
        },
    )
    return _envelope(derivative_dto.AssetPositionCloseDerivativeResponse, payload)


def get_asset_position_open(
    account_id: str,
    sub_account_id: str,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.AssetPositionOpenDerivativeResponse]:
    """Get open derivatives positions.

    Operation 6.3 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/position-open/
    """
    payload = request_api.get(
        "/khronos/v1/account/portfolio/status",
        token,
        params={"accountId": account_id, "subAccountId": sub_account_id},
    )
    return _envelope(derivative_dto.AssetPositionOpenDerivativeResponse, payload)


def get_list_order_normal(
    page_no: int,
    page_size: int,
    account_id: str,
    symbol: str,
    order_type: str,
    status: str,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.ListOrderNormalDerivativeResponse]:
    """Get the derivatives order book for one day.

    Operation 6.6 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/get-normal-orders/
    """
    payload = request_api.get(
        "/khronos/v1/order/in-day",
        token,
        params={
            "pageNo": page_no,
            "pageSize": page_size,
            "accountId": account_id,
            "symbol": symbol,
            "orderType": order_type,
            "status": status,
        },
    )
    return _envelope(derivative_dto.ListOrderNormalDerivativeResponse, payload)


def get_list_order_condition(
    page_no: int,
    page_size: int,
    account_id: str,
    sub_account_id: str,
    order_status: str,
    order_type: str,
    symbol: str,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.ListOrderConditionDerivativeResponse]:
    """Get the derivatives conditional-order book.

    Operation 6.7 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/get-condition-orders/

    The query keys for this endpoint are inconsistently cased by TCBS
    (``PageSize``/``subAccountID``/``Symbol``); they are reproduced as-is.
    """
    payload = request_api.get(
        "/khronos/v1/order/condition/detail",
        token,
        params={
            "pageNo": page_no,
            "PageSize": page_size,
            "accountId": account_id,
            "subAccountID": sub_account_id,
            "orderStatus": order_status,
            "orderType": order_type,
            "Symbol": symbol,
        },
    )
    return _envelope(derivative_dto.ListOrderConditionDerivativeResponse, payload)


def place_order(
    request_dto: derivative_dto.PlaceOrderDto,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.OrderNormalDerivativeResponse]:
    """Place a derivatives order.

    Operation 6.4 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/place-order/
    """
    payload = request_api.post("/khronos/v1/order/place", token, body=asdict(request_dto))
    return _envelope(derivative_dto.OrderNormalDerivativeResponse, payload)


def place_order_condition(
    request_dto: derivative_dto.OrderConditionDerivativeRequestDTO,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.OrderConditionDerivativeResponseDTO]:
    """Place a derivatives conditional order.

    Operation 6.5 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/place-condition-order/
    """
    payload = request_api.post("/khronos/v1/order/condition/place", token, body=asdict(request_dto))
    return _envelope(derivative_dto.OrderConditionDerivativeResponseDTO, payload)


def edit_place_order(
    request_dto: derivative_dto.EditOrderNormalDerivativeRequestDTO,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.EditOrderNormalDerivativeResponseDTO]:
    """Amend a derivatives order.

    Operation 6.8 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/update-order/
    """
    payload = request_api.post("/khronos/v1/order/change", token, body=asdict(request_dto))
    return _envelope(derivative_dto.EditOrderNormalDerivativeResponseDTO, payload)


def edit_place_order_condition(
    request_dto: derivative_dto.EditOrderConditionDerivativeRequestDTO,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.EditOrderConditionDerivativeResponseDTO]:
    """Amend a derivatives conditional order.

    Operation 6.9 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/update-condition-order/
    """
    payload = request_api.post("/khronos/v2/order/condition/change", token, body=asdict(request_dto))
    return _envelope(derivative_dto.EditOrderConditionDerivativeResponseDTO, payload)


def cancel_place_order(
    request_dto: derivative_dto.CancelOrderNormalDerivativeRequestDTO,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.CancelOrderNormalDerivativeResponseDTO]:
    """Cancel a derivatives order.

    Operation 6.10 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/cancel-order/
    """
    payload = request_api.post("/khronos/v1/order/cancel", token, body=asdict(request_dto))
    return _envelope(derivative_dto.CancelOrderNormalDerivativeResponseDTO, payload)


def cancel_place_order_condition(
    request_dto: derivative_dto.CancelOrderConditionDerivativeRequestDTO,
    token: str,
) -> derivative_dto.DerivativeResponse[derivative_dto.CancelOrderConditionDerivativeResponseDTO]:
    """Cancel a derivatives conditional order.

    Operation 6.11 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/cancel-condition-order/
    """
    payload = request_api.post("/khronos/v1/order/condition/cancel", token, body=asdict(request_dto))
    return _envelope(derivative_dto.CancelOrderConditionDerivativeResponseDTO, payload)


def market_information_bid_ask(token: str) -> derivative_dto.MarketInformationResponseDTO:
    """Get the derivatives price board, with best bid and offer levels.

    Operation 7.1 — https://developers.tcbs.com.vn/docs/v1.0.0/derivative/market-symbol/

    Unlike its neighbours in this module, this endpoint returns a bare object rather than
    an envelope, so it is decoded with ``dacite``.
    """
    payload = request_api.get("/tartarus/v1/derivatives", token)
    return request_api.decode(derivative_dto.MarketInformationResponseDTO, payload)

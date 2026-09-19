"""Move cash between sub-accounts, and in or out of the derivatives margin account."""

from __future__ import annotations

from dataclasses import asdict

from tcbs_api.dto.money import money
from tcbs_api.utils import request_api


def transfer_between_subaccounts(
    request_dto: money.TransferBetweenSubaccountRequestDTO,
    token: str,
) -> money.TransferBetweenSubaccountResponseDTO:
    """Transfer cash between two sub-accounts of the same custody account.

    Operation 3.1 — https://developers.tcbs.com.vn/docs/v1.0.0/money/transfer/
    """
    payload = request_api.post("/physis/v1/stock/transfer", token, body=asdict(request_dto))
    return request_api.decode(money.TransferBetweenSubaccountResponseDTO, payload)


def withdrawal_margin(
    request_dto: money.WithdrawalDerivativeRequestDTO,
    token: str,
) -> money.WithdrawalDerivativeResponseDTO:
    """Request a withdrawal from the derivatives margin account.

    Operation 3.2 — https://developers.tcbs.com.vn/docs/v1.0.0/money/withdraw/
    """
    payload = request_api.post("/khronos/v1/cash/withdraw/update", token, body=asdict(request_dto))
    return request_api.decode(money.WithdrawalDerivativeResponseDTO, payload)


def deposit_margin(
    request_dto: money.DepositDerivativeRequestDTO,
    token: str,
) -> money.DepositDerivativeMarginResponseDTO:
    """Request a deposit into the derivatives margin account.

    Operation 3.3 — https://developers.tcbs.com.vn/docs/v1.0.0/money/deposit/
    """
    payload = request_api.post("/khronos/v1/cash/deposit/update", token, body=asdict(request_dto))
    return request_api.decode(money.DepositDerivativeMarginResponseDTO, payload)

"""Cash-transfer and margin deposit/withdrawal models.

The ``*RequestDTO`` models are the bodies sent to TCBS, serialized with
:func:`dataclasses.asdict`; the ``*ResponseDTO`` models are what comes back. The margin
``data`` payload is an untyped object in the document, so it stays a plain ``dict``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TransferBetweenSubaccountRequestDTO:
    sourceAccountNumber: str
    destinationAccountNumber: str
    amount: float
    description: str


@dataclass
class TransferBetweenSubaccountResponseDTO:
    code: str
    message: str


@dataclass
class WithdrawalDerivativeRequestDTO:
    accountId: str
    subAccountId: str
    amount: float
    paymentContent: str | None = None


@dataclass
class WithdrawalDerivativeResponseDTO:
    cmd: str
    rc: str
    rs: str | None = None
    oID: str | None = None
    data: dict | None = None


@dataclass
class DepositDerivativeRequestDTO:
    accountId: str
    subAccountId: str
    amount: float
    paymentContent: str | None = None


@dataclass
class DepositDerivativeMarginResponseDTO:
    cmd: str
    rc: str
    rs: str | None = None
    oID: str | None = None
    data: dict | None = None

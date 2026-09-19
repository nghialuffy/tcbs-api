"""Profile information for a sub-account, as returned by ``get_subaccount_info``.

The endpoint's ``fields`` query parameter decides which parts come back, so both documented
keys are optional: ask for ``basicInfo,bankSubAccounts`` and you get those two. The spec
describes ``basicInfo`` only as an object, so it stays a plain ``dict``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BankSubAccount:
    """One sub-account of the custody account."""

    accountNo: str
    accountName: str
    accountType: str
    accountTypeName: str
    status: str
    isDefault: str
    bankCode: str | None = None


@dataclass
class AccountInformationResponse:
    """Response of ``get_subaccount_info`` (operation 2.1)."""

    basicInfo: dict | None = None
    bankSubAccounts: list[BankSubAccount] | None = None

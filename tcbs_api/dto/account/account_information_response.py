"""Profile information for a sub-account, as returned by ``get_subaccount_info``.

``BasicInfo``, ``PersonalInfo``, ``BankAccount`` and ``BankSubAccount`` are only populated
when they are named in the endpoint's ``fields`` query parameter; the others come back as
``None``.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BasicInfo:
    tcbsId: str | None = None
    code105C: str | None = None
    status: str | None = None
    type: str | None = None
    depository: bool | None = None


@dataclass
class PersonalInfo:
    fullName: str | None = None
    fullNameNoAccent: str | None = None
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    phoneNumber: str | None = None
    gender: str | None = None
    birthday: str | None = None
    contactAddress: str | None = None
    permanentAddress: str | None = None
    nationality: str | None = None
    nationalityName: str | None = None
    taxIdNumber: str | None = None
    acronym: str | None = None
    createdDate: str | None = None
    updatedDate: str | None = None
    flowOpenAccount: str | None = None
    avatarUrl: str | None = None
    businessType: str | None = None
    ppBusinessType: str | None = None
    ppBusinessField: str | None = None
    ppBusinessTypeName: str | None = None
    ppBusinessFieldName: str | None = None
    identityCard: dict | None = None


@dataclass
class BankAccount:
    accountNo: str | None = None
    accountName: str | None = None
    accountNameNoAccent: str | None = None
    bankCode: str | None = None
    bankName: str | None = None
    branchCode: str | None = None
    bankType: str | None = None
    bankSys: str | None = None
    authorized: bool | None = None
    bankAccountType: str | None = None


@dataclass
class BankSubAccount:
    accountNo: str | None = None
    accountName: str | None = None
    accountType: str | None = None
    accountTypeName: str | None = None
    status: str | None = None
    isDefault: str | None = None


@dataclass
class AccountInformationResponse:
    basicInfo: BasicInfo | None = None
    personalInfo: PersonalInfo | None = None
    bankAccounts: list[BankAccount] | None = field(default_factory=list)
    bankSubAccounts: list[BankSubAccount] | None = field(default_factory=list)

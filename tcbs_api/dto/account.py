"""Profile information for a sub-account, as returned by ``get_subaccount_info``.

The endpoint's ``fields`` query parameter decides which parts come back, so every block —
``basicInfo``, ``personalInfo``, ``personalBasicInfo``, ``accountStatus``, ``bankAccounts``,
``bankSubAccounts``, ``systemUserInfo`` and ``rmRefInfo`` — is optional and defaults to
``None``. Fields also accepts a block's sub-field, as in ``personalInfo:fullName``, which
returns a partial block; for that reason **every field of every model here is optional with
a ``None`` default**, unlike the rest of `tcbs_api.dto`, where scalars are declared
without defaults.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from tcbs_api.dto.base import DtoModel


class IdentityCard(DtoModel):
    """The ``identityCard`` block of ``personalInfo``."""

    idNumber: str | None = Field(default=None, description="Identity-card number.")
    idPlace: str | None = Field(default=None, description="Issuing authority, e.g. Bộ Công an.")
    idDate: str | None = Field(default=None, description="Issue date.")
    expireDate: str | None = Field(default=None, description="Expiry date.")
    idType: str | None = Field(default=None, description="Identity document type code.")


class PersonalInfo(DtoModel):
    """Holder personal details."""

    firstName: str | None = Field(default=None, description="Given name.")
    lastName: str | None = Field(default=None, description="Family name.")
    fullName: str | None = Field(default=None, description="Full name, with diacritics.")
    fullNameNoAccent: str | None = Field(default=None, description="Full name without diacritics.")
    email: str | None = Field(default=None, description="Email address.")
    phoneNumber: str | None = Field(default=None, description="Phone number.")
    avatarData: Any = Field(
        default=None,
        description="Raw avatar payload — null in the sampled response, so its shape is unknown.",
    )
    avatarUrl: str | None = Field(default=None, description="Public avatar URL.")
    identityCard: IdentityCard | None = Field(default=None, description="Identity-card details.")


class AccountStatus(DtoModel):
    """Activation state of each service the custody account can use."""

    fundActivationStatus: str | None = Field(
        default=None,
        description="Whether the fund-certificate service is active: 1 = active.",
    )
    fundActivationDate: str | None = Field(default=None, description="When the fund-certificate service was activated.")
    fundAccount: str | None = Field(default=None, description="Fund-certificate sub-account number.")
    flexActivationStatus: str | None = Field(
        default=None,
        description="Whether the flex service is active: 1 = active.",
    )
    flexActivationDate: str | None = Field(default=None, description="When the flex service was activated.")
    flexAccount: str | None = Field(default=None, description="Flex sub-account number.")
    privatePlacementActivationStatus: str | None = Field(
        default=None,
        description="Whether private-placement trading is active: 1 = active.",
    )
    privatePlacementActivationDate: str | None = Field(
        default=None,
        description="When private-placement trading was activated.",
    )
    derivativeActivationStatus: str | None = Field(
        default=None,
        description="Whether derivatives trading is active: 1 = active.",
    )
    derivativeActivationDate: str | None = Field(default=None, description="When derivatives trading was activated.")
    tcBondAccount: str | None = Field(default=None, description="TCBS bond sub-account number.")
    transferStatus: str | None = Field(default=None, description="Whether cash transfers are allowed: 1 = allowed.")
    confirmed105CStatus: str | None = Field(
        default=None,
        description="Whether the 105C contract was confirmed, e.g. CONFIRMED.",
    )
    docusignStatus: str | None = Field(default=None, description="Docusign state — null in the sampled payload.")
    onboardingStatus: str | None = Field(default=None, description="Onboarding state — null in the sampled payload.")
    tccAccountStatus: str | None = Field(default=None, description="TCC custody account status code.")
    hnxActivationStatus: str | None = Field(
        default=None,
        description="HNX activation state — null in the sampled payload.",
    )
    hnxAccount: str | None = Field(default=None, description="HNX sub-account number — null in the sampled payload.")
    caStatus: str | None = Field(default=None, description="Corporate-action status, e.g. IGNORE.")


class BasicInfo(DtoModel):
    """Basic account information."""

    tcbsId: str | None = Field(default=None, description="TCBS customer id.")
    code105C: str | None = Field(default=None, description="105C contract code.")
    status: str | None = Field(default=None, description="Account status, e.g. ACTIVE.")
    type: str | None = Field(default=None, description="Account type, e.g. INDIVIDUAL.")
    depository: bool | None = Field(default=None, description="Whether the account uses TCBS's depository service.")


class BankAccount(DtoModel):
    """One bank account linked to the custody account."""

    bankAccountId: int | None = Field(default=None, description="TCBS's internal id for the link.")
    accountNo: str | None = Field(default=None, description="Bank account number.")
    accountName: str | None = Field(default=None, description="Holder name as the bank has it.")
    accountNameNoAccent: str | None = Field(default=None, description="Holder name without diacritics.")
    bankCode: str | None = Field(default=None, description="Bank code.")
    bankName: str | None = Field(default=None, description="Bank name.")
    bankProvince: str | None = Field(default=None, description="Province the account is registered in.")
    branchCode: str | None = Field(default=None, description="Branch, as the bank names it.")
    bankType: str | None = Field(default=None, description="How the link is used, e.g. CENTRALIZED_PAYMENT.")
    bankSys: str | None = Field(default=None, description="Bank system code.")
    bankAccountType: str | None = Field(default=None, description="Account type, e.g. STOCK_FUND.")
    authorized: bool | None = Field(
        default=None,
        description="Whether the account is authorized — null in the sampled payload.",
    )
    rootBankProvince: str | None = Field(
        default=None,
        description="Province of the root account; null when the branch is the root.",
    )
    rootBranchCode: str | None = Field(default=None, description="Root branch code; null when the branch is the root.")
    rootBankCode: str | None = Field(default=None, description="Root bank code.")
    rootBankName: str | None = Field(default=None, description="Root bank name, in short form.")
    insType: str | None = Field(default=None, description="Institution type, e.g. LOCAL.")
    isVirtualAccount: int | None = Field(
        default=None,
        description="Whether this is a virtual account: 0 = no, 1 = yes.",
    )


class BankSubAccount(DtoModel):
    """One sub-account of the custody account."""

    accountNo: str = Field(description="Sub-account number.")
    accountName: str = Field(description="Account holder name.")
    accountType: str = Field(description="Sub-account type: NORMAL, MARGIN, DERIVATIVE.")
    accountTypeName: str = Field(description="Sub-account type name.")
    status: str = Field(description="Sub-account status.")
    isDefault: str = Field(description="Whether this is the default sub-account (Y/N).")
    bankCode: str | None = Field(default=None, description="Bank code (may be null).")


class SystemUserInfo(DtoModel):
    """Which internal system user, if any, is linked to the account."""

    systemUserType: str | None = Field(
        default=None,
        description="Type of internal user linked to the account, e.g. UNKNOW.",
    )
    systemUser: str | None = Field(
        default=None,
        description="Name of the internal user linked to the account, e.g. UNKNOW.",
    )


class AccountInformationResponse(DtoModel):
    """Response of ``get_subaccount_info`` (operation 2.1)."""

    basicInfo: BasicInfo | None = Field(default=None, description="Basic account information.")
    personalInfo: PersonalInfo | None = Field(default=None, description="Holder personal details.")
    personalBasicInfo: dict | None = Field(
        default=None,
        description="Basic personal fields, kept a raw dict: no sample documented its shape.",
    )
    accountStatus: AccountStatus | None = Field(
        default=None,
        description="Service activation state of the custody account.",
    )
    bankAccounts: list[BankAccount] | None = Field(
        default=None,
        description="Bank accounts linked to the custody account.",
    )
    bankSubAccounts: list[BankSubAccount] | None = Field(default=None, description="List of sub-accounts.")
    systemUserInfo: SystemUserInfo | None = Field(
        default=None,
        description="Internal system user linked to the account, if any.",
    )
    rmRefInfo: list[dict] | None = Field(
        default=None,
        description="Relationship-manager references, a list of raw dicts — no sample documented their shape.",
    )

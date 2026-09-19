"""Read profile information for a sub-account."""

from __future__ import annotations

from tcbs_api.dto.account import AccountInformationResponse
from tcbs_api.utils import request_api

PROFILE_FIELDS = (
    "basicInfo,personalInfo,personalBasicInfo,personalInfo:fullName,accountStatus,"
    "bankAccounts,bankSubAccounts,systemUserInfo,rmRefInfo"
)


def get_subaccount_info(custody_code: str, fields: str, token: str) -> AccountInformationResponse:
    """Get the profile information of a sub-account.

    Operation 2.1 — https://developers.tcbs.com.vn/docs/v1.0.0/account/sub-account/

    `fields` selects which blocks to return, as a comma-separated list, for example
    ``"basicInfo,personalInfo,bankSubAccounts,bankAccounts"``. The blocks are
    ``basicInfo``, ``personalInfo``, ``personalBasicInfo``, ``accountStatus``,
    ``bankAccounts``, ``bankSubAccounts``, ``systemUserInfo`` and ``rmRefInfo``; the ones
    that are not requested come back as ``None``.

    A block can also be narrowed to a single field with ``block:field``, as in
    ``"personalInfo:fullName"``, which returns a partial block — so every field is
    optional, not just the block itself.
    """
    fields = fields or PROFILE_FIELDS
    payload = request_api.get(f"/eros/v2/get-profile/by-username/{custody_code}", token, params={"fields": fields})
    return request_api.decode(AccountInformationResponse, payload)

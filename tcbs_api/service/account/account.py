"""Read profile information for a sub-account."""

from __future__ import annotations

from tcbs_api.dto.account.account import AccountInformationResponse
from tcbs_api.utils import request_api


def get_subaccount_info(custody_code: str, fields: str, token: str) -> AccountInformationResponse:
    """Get the profile information of a sub-account.

    Operation 2.1 — https://developers.tcbs.com.vn/docs/v1.0.0/account/sub-account/

    `fields` selects which blocks to return, as a comma-separated list, for example
    ``"basicInfo,personalInfo,bankSubAccounts,bankAccounts"``. Blocks that are not
    requested come back as ``None``.
    """
    payload = request_api.get(f"/eros/v2/get-profile/by-username/{custody_code}", token, params={"fields": fields})
    return request_api.decode(AccountInformationResponse, payload)

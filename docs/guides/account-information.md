# Account information

`get_subaccount_info` returns the profile TCBS holds for a custody account — operation 2.1.

```python
from tcbs_api.service import account as account_service

info = account_service.get_subaccount_info(custody_code, "basicInfo,personalInfo", token)
print(info.basicInfo.tcbsId, info.personalInfo.fullName)
```

## The `fields` parameter

The endpoint decides which blocks of the profile to send from the `fields` query parameter, a
comma-separated list. A block you do not ask for is simply absent, so it stays `None` on the
model:

```python
info = account_service.get_subaccount_info(custody_code, "basicInfo", token)

info.basicInfo  # BasicInfo — populated
info.personalInfo  # None — not requested
info.bankSubAccounts  # None — not requested
```

The blocks are:

| Block | Contents |
| --- | --- |
| `basicInfo` | Custody and account identifiers, branch and broker |
| `personalInfo` | Holder details, including the `identityCard` block |
| `personalBasicInfo` | A second, thinner copy of the personal block |
| `accountStatus` | Which services are active on the account |
| `bankAccounts` | Registered bank accounts |
| `bankSubAccounts` | Bank sub-accounts money can move to |
| `systemUserInfo` | System-user record |
| `rmRefInfo` | Relationship-manager reference |

A block can also be narrowed to a single field with `block:field`:

```python
info = account_service.get_subaccount_info(custody_code, "personalInfo:fullName", token)
print(info.personalInfo.fullName)  # populated
print(info.personalInfo.email)  # None
```

Because a narrowed block comes back partial, **every field of every model in this domain is
optional** with a `None` default — unlike the rest of [`tcbs_api.dto`](../api/models.md#tcbs_api.dto),
where a scalar the API always sends is declared without a default.

## Asking for everything

An empty `fields` string falls back to `PROFILE_FIELDS`, the library's constant, which asks for
all eight blocks and narrows `personalInfo` to its `fullName` field:

```python
info = account_service.get_subaccount_info(custody_code, "", token)
```

## Where the identifiers are

The response is exactly the eight blocks and nothing else — there is no top-level account
number, so read identifiers out of the block that carries them:

```python
print(info.basicInfo.tcbsId, info.basicInfo.status)
```

## Reference

- [`tcbs_api.service.account`](../api/services.md#tcbs_api.service.account) — the function
- [`tcbs_api.dto.account`](../api/models.md#tcbs_api.dto.account) — every model and field of this domain

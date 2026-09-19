# tcbs-api

Python client library for the [TCBS Open API](https://developers.tcbs.com.vn/).

Thin, dependency-light wrapper over the TCBS REST endpoints: authentication, account
information, cash transfers, stock (normal) trading, and derivatives trading. Responses
are parsed into typed `dataclass` DTOs with `dacite`, so you get autocompletion instead
of hand-written `dict` poking.

The one exception is the derivative endpoints, whose response envelope is typed but whose
`data` payload is left as a raw `dict` — see [Known limitations](#known-limitations).

- Distribution name: `tcbs-api`
- Import package: `tcbs_api`
- Source code: <https://github.com/nghialuffy/tcbs-api>
- Issue tracker: <https://github.com/nghialuffy/tcbs-api/issues>
- Official API docs: <https://developers.tcbs.com.vn/>

## Requirements

- Python 3.10 or newer
- A TCBS Open API key (obtain it from the [TCBS developer portal](https://developers.tcbs.com.vn/))

## Installation

With [uv](https://docs.astral.sh/uv/):

```bash
uv add tcbs-api
```

With pip:

```bash
pip install tcbs-api
```

From a source checkout (either tool):

```bash
uv add git+https://github.com/nghialuffy/tcbs-api
pip install git+https://github.com/nghialuffy/tcbs-api
```

For development, install the lint/type-check extras:

```bash
uv sync --extra dev    # or: pip install -e ".[dev]"
```

## Quick start

```python
from tcbs_api.dto import money as money_dto
from tcbs_api.service.account import account as account_service
from tcbs_api.service.auth import token as token_service
from tcbs_api.service.money import money as money_service

API_KEY = "your-api-key"
OTP = "your-otp"

# 1.1. Exchange the API key for a JWT token.
# NOTE: this endpoint is rate limited to 10 requests/day — persist the token
# and reuse it instead of calling this on every request.
token = token_service.get_token(API_KEY, OTP).token

# 2.1. Account information.
custody_code = "0001201435"
info = account_service.get_subaccount_info(
    custody_code,
    "basicInfo,personalInfo,bankSubAccounts,bankAccounts",
    token,
)
print(info.personalInfo.fullName)

# 3.1. Transfer money between sub-accounts.
request_dto = money_dto.TransferBetweenSubaccountRequestDTO(
    sourceAccountNumber="105C336655A",
    destinationAccountNumber="0001201435",
    amount=10_000,
    description="CHUYEN TIEN PHAI SINH",
)
result = money_service.transfer_between_subaccounts(request_dto, token)
print(result.code, result.message)
```

## Placing an order

```python
from tcbs_api.dto.stock_normal import stock_normal_dto
from tcbs_api.service.stock_normal import normal as stock_service

request_dto = stock_normal_dto.PlaceOrderExternalDto(
    execType="NS",
    price=1000,
    priceType="LO",
    quantity=100,
    symbol="FPT",
)
response = stock_service.place_order(request_dto, account_no="0001201435", token=token)
print(response.orderId)
```

## API reference

The public API mirrors the numbering used in the TCBS documentation. Every function takes
the JWT `token` as its last positional argument, and each carries a docstring naming the
operation it implements and linking that page — so `help(tcbs_api.service.stock_normal.normal)`
and IDE hover text both tell you where to look.

| Module | Covers |
| --- | --- |
| `tcbs_api.service.auth` | Exchange an API key for a JWT token (1.1) |
| `tcbs_api.service.account` | Account information (2.1) |
| `tcbs_api.service.money` | Internal transfers, margin deposit and withdrawal (3.x) |
| `tcbs_api.service.stock_normal` | Stock order lifecycle, purchasing power, assets (4.x) |
| `tcbs_api.service.derivative` | Derivatives cash, positions, orders (6.x), market data (7.1) |

Request and response models live under `tcbs_api.dto`, grouped by the same domains.

## Error handling

Non-2xx responses call `requests.Response.raise_for_status()`, so HTTP failures surface
as `requests.HTTPError`:

```python
import requests

from tcbs_api.service.stock_normal import normal as stock_service

try:
    response = stock_service.get_orders(account_no="0001201435", token=token)
except requests.HTTPError as exc:
    print(exc.response.status_code, exc.response.json())
```

## Development

```bash
git clone https://github.com/nghialuffy/tcbs-api
cd tcbs-api

uv sync --extra dev
uv run ruff check .
uv run ruff format --check .
uv run mypy tcbs_api
uv build
```

## Releasing

Publishing is automated by
[`.github/workflows/publish.yml`](https://github.com/nghialuffy/tcbs-api/blob/main/.github/workflows/publish.yml)
using PyPI [trusted publishing](https://docs.pypi.org/trusted-publishers/) (OIDC), so no
API token is stored in this repository.

### One-time setup

On PyPI, go to **Account → Publishing → Add a pending publisher** and fill in:

| Field | Value |
| --- | --- |
| PyPI project name | `tcbs-api` |
| Owner | `nghialuffy` |
| Repository name | `tcbs-api` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

The environment name must match the `environment:` key in the publish job.

### Cutting a release

`tcbs_api/__init__.py` is the single source of truth for the version — `pyproject.toml`
reads it dynamically, so there is nothing to keep in sync.

1. Bump `__version__` in `tcbs_api/__init__.py` and add a matching `CHANGELOG.md` entry.
2. Commit, then tag and push:
   ```bash
   git commit -am "release: vX.Y.Z"
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin main --follow-tags
   ```
3. Publish a GitHub Release for that tag. The workflow builds the sdist and wheel, runs
   `twine check --strict`, verifies the built version matches the tag, and uploads to
   PyPI.

Because `tcbs-api` does not exist on PyPI yet, the first release needs a **pending**
publisher as shown above. Once the project exists, the same entry is managed from the
project's own settings instead.

### Rehearsing on TestPyPI

Run the same commands against TestPyPI before a real release:

```bash
uv build
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-<testpypi-token>
```

### Notes

- A published version can **never** be re-uploaded, so bump `__version__` for every
  attempt — including failed ones. The tag/version guard in the workflow catches the
  common slip of tagging a version you forgot to bump.
- Keep the tag (with a `v` prefix) in sync with `__version__` (no `v`); the workflow
  strips the prefix before comparing.

## Known limitations

### Derivative payloads are not typed

The derivative endpoints return a `DerivativeResponse` envelope, but its generic `data`
field stays a raw `dict`. `dataclasses_json` cannot resolve the `Generic[T]` parameter —
it warns `Unknown type ~T at DerivativeResponse.data` — so the declared element type is
never applied:

```python
from tcbs_api.dto.derivative_dto import TotalCashDerivativeResponse
from tcbs_api.service.derivative import derivative as derivative_service

envelope = derivative_service.get_total_cash_derivative(account_id, sub_account_id, "0", token)
type(envelope)        # <class 'tcbs_api.dto.derivative_dto.derivative_dto.DerivativeResponse'>
type(envelope.data)   # <class 'dict'>

# Decode the payload yourself to get the typed object:
cash = TotalCashDerivativeResponse.from_dict(envelope.data, infer_missing=True)
```

### `Optional[...]` fields have no defaults

Many DTO fields are annotated `Optional[...]` but are not given a `= None` default, so
`dataclasses_json`'s `from_dict`/`from_json` raise `KeyError` when a field is missing from
the payload. Pass `infer_missing=True` (as above) to tolerate missing keys. Decoding in
the library itself is unaffected, because the non-derivative endpoints use `dacite` with
`Config(strict=False)`.

### Operational notes

- The token endpoint is limited to **10 requests per day** by TCBS; cache the token.
- The library performs no retries, rate limiting, or token refresh — callers own that
  policy.
- Requests are issued synchronously with `requests`. There is no async client.

## License

MIT — see [LICENSE](https://github.com/nghialuffy/tcbs-api/blob/main/LICENSE).

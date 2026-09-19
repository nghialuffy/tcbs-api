# tcbs-api

Python client library for the [TCBS Open API](https://developers.tcbs.com.vn/).

Thin, dependency-light wrapper over the TCBS REST endpoints: authentication, account
information, cash transfers, stock (normal) trading, cash-market data, and derivatives
trading. Responses are parsed into typed `dataclass` DTOs with `dacite`, so you get
autocompletion instead of hand-written `dict` poking.

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

# 2.1. Account information. The `fields` parameter decides what comes back;
#       `basicInfo` is a plain dict and `bankSubAccounts` a list of records.
custody_code = "0001201435"
info = account_service.get_subaccount_info(
    custody_code,
    "basicInfo,bankSubAccounts",
    token,
)
print(info.bankSubAccounts[0].accountNo, info.basicInfo["tcbsId"])

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
from tcbs_api.dto.stock_normal import stock_normal
from tcbs_api.service.stock_normal import normal as stock_service

request_dto = stock_normal.PlaceOrderExternalDto(
    execType="NS",
    price=1000,
    priceType="LO",
    quantity=100,
    symbol="FPT",
)
response = stock_service.place_order(request_dto, account_no="0001201435", token=token)
print(response.orderId)
```

## Reading market data

```python
from tcbs_api.service.market import market as market_service

# Symbol and price board: a basket, or an explicit list of symbols (the two are
# mutually exclusive, and are keyword-only because `token` comes first here).
board = market_service.get_symbol_and_price(token, index=1)
print(board.tradingDate, board.data[0].matchPrice)

# Supply and demand, filtered by investor class — here `token` stays a positional
# argument, since the symbol is required.
flow = market_service.get_supply_demand_daily("FPT", token, investor_type="shark")
print(flow.data[-1].bsr)
```

## API reference

The public API mirrors the numbering used in the TCBS documentation. Each function carries
a docstring naming the operation it implements and linking that page — so
`help(tcbs_api.service.stock_normal.normal)` and IDE hover text both tell you where to look.

Where every argument other than `token` is an optional filter, `token` comes **first** and the
filters are keyword-only (`None` values are dropped from the query); everywhere else `token`
stays the last positional argument.

| Module | Covers |
| --- | --- |
| `tcbs_api.service.auth` | Exchange an API key for a JWT token (1.1) |
| `tcbs_api.service.account` | Account information (2.1) |
| `tcbs_api.service.money` | Internal transfers, margin deposit and withdrawal (3.x) |
| `tcbs_api.service.stock_normal` | Stock order lifecycle, purchasing power, assets, cash balance and cash statement (4.x) |
| `tcbs_api.service.market` | Cash-market price board, foreign room, put-through, intraday and supply-and-demand data (5.x) |
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

### The models mirror the document, so three things follow

Every DTO field comes from `openapi-v1.0.0.json` for the operation that returns it — no
inferred fields:

- **Payloads the document leaves untyped stay `dict`s** — the derivative `data` for 6.1 and
  6.11, and the `data` of the two margin operations:

  ```python
  from tcbs_api.service.derivative import derivative as derivative_service

  envelope = derivative_service.get_total_cash_derivative(account_id, sub_account_id, "0", token)
  type(envelope.data)  # <class 'dict'> — the document lists no fields for it
  ```

  5.11 is the extreme case: the document gives it no response at all, so `get_securities_info`
  returns the JSON body undecoded.
- **Containers default to `None`.** The document marks no response field required, so scalars
  decode as-is while `orders`, `data`, `assets`, `response` and friends can be `None` — an
  empty collection can arrive as an omitted key, and `dacite` raises for a declared field the
  payload omits.
- **`int64` is `int`, `number` is `float`** — so `PriceMatchingHistoryResponse.total` is a
  `float` even though it counts matches. `dacite` accepts an integer for a `float` field but
  not a float for an `int` field, which is why anything the document does not pin to `int64`
  is a `float`.

### `Optional[...]` fields in the derivative models have no defaults

The derivative models are decoded with `dataclasses_json`, which raises `KeyError` for a
missing field unless it has a `= None` default. Pass `infer_missing=True` to tolerate missing
keys (and extra ones):

```python
from tcbs_api.dto.derivative import ListOrderNormalDerivativeResponse

raw = envelope.data[0]
order = ListOrderNormalDerivativeResponse.from_dict(raw, infer_missing=True)
```

### Operational notes

- The token endpoint is limited to **10 requests per day** by TCBS; cache the token.
- The library performs no retries, rate limiting, or token refresh — callers own that
  policy.
- Requests are issued synchronously with `requests`. There is no async client.

## License

MIT — see [LICENSE](https://github.com/nghialuffy/tcbs-api/blob/main/LICENSE).

# tcbs-api

Python client library for the [TCBS Open API](https://developers.tcbs.com.vn/).

Thin, dependency-light wrapper over the TCBS REST read endpoints: authentication, account
information, stock order and trade lookups, holdings, cash, and cash-market data. Responses are
parsed into typed [pydantic](https://docs.pydantic.dev/) models, so you get autocompletion
instead of hand-written `dict` poking.

The nine endpoints that place, amend or cancel an order — and the three that move cash — are
deliberately not wrapped, and neither is any derivative endpoint; see
[Known limitations](#known-limitations).

A few payloads stay partly raw — the profile blocks no real payload pinned down — see
[Known limitations](#known-limitations).

- Distribution name: `tcbs-api`
- Import package: `tcbs_api`
- Documentation: <https://tcbs-api.readthedocs.io/>
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

For development, install the lint, type-check and docs extras:

```bash
uv sync    # or: pip install -e ".[dev,docs]" — ruff, mypy, pytest and the MkDocs stack
```

## Quick start

```python
from tcbs_api.service import account as account_service, token as token_service

API_KEY = "your-api-key"
OTP = "your-otp"

# 1.1. Exchange the API key for a JWT token.
# NOTE: this endpoint is rate limited to 10 requests/day — persist the token
# and reuse it instead of calling this on every request.
token = token_service.get_token(API_KEY, OTP).token

# 2.1. Account information. The `fields` parameter decides which blocks come back;
#       a block you leave out stays None, and `block:field` narrows one further.
custody_code = "0001201435"
info = account_service.get_subaccount_info(
    custody_code,
    "basicInfo,personalInfo:fullName,bankSubAccounts",
    token,
)
print(info.bankSubAccounts[0].accountNo, info.basicInfo.tcbsId, info.personalInfo.fullName)
```

## Reading holdings and cash

```python
from tcbs_api.service import stock as stock_service

# 4.14. Every stock the sub-account holds, with what is sellable today.
holdings = stock_service.get_asset_stock_by_sub_account("0001F77149", token)
for holding in holdings.stock:
    print(holding.symbol, holding.availableTrading, holding.currentPrice, holding.totalQtty)

# 4.15. The same account's cash: balance, buying power and what is blocked.
cash = stock_service.get_cash_investment("0001F77149", token)
print(cash.data[0].balance, cash.data[0].pp0, cash.data[0].blockAmountInfo.blockAmountTotal)
```

## Reading market data

```python
from tcbs_api.service import market as market_service

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
`help(tcbs_api.service.stock.get_orders)` and IDE hover text both tell you where to look.

Where every argument other than `token` is an optional filter, `token` comes **first** and the
filters are keyword-only (`None` values are dropped from the query); everywhere else `token`
stays the last positional argument.

| Module | Covers |
| --- | --- |
| `tcbs_api.service.token` | Exchange an API key for a JWT token (1.1) |
| `tcbs_api.service.account` | Account information (2.1) |
| `tcbs_api.service.stock` | Stock orders, trades, purchasing power, holdings, cash balance and cash statement (4.x) |
| `tcbs_api.service.market` | Cash-market price board, foreign room, put-through, intraday and supply-and-demand data (5.x) |

Request and response models live under `tcbs_api.dto`, grouped by the same domains. The
generated reference — signatures, models and all 437 field descriptions — is at
<https://tcbs-api.readthedocs.io/api/>.

The endpoints that write — placing, amending and cancelling orders, and moving cash — are not
wrapped, so no function here changes anything at TCBS. `get_token` is the only call that issues
a `POST`, and it only exchanges the API key for a token. The derivatives endpoints (6.x and 7.1)
are not wrapped either.

## Error handling

Non-2xx responses call `requests.Response.raise_for_status()`, so HTTP failures surface
as `requests.HTTPError`:

```python
import requests

from tcbs_api.service import stock as stock_service

try:
    response = stock_service.get_orders(account_no="0001201435", token=token)
except requests.HTTPError as exc:
    print(exc.response.status_code, exc.response.json())
```

## Development

```bash
git clone https://github.com/nghialuffy/tcbs-api
cd tcbs-api

uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy tcbs_api
uv build
```

The documentation under <https://tcbs-api.readthedocs.io/> is built by MkDocs from `docs/` and
`mkdocs.yml`, with the API reference generated from the docstrings by mkdocstrings. Preview it
locally with:

```bash
uv run mkdocs serve    # http://127.0.0.1:8000
uv run mkdocs build --strict
```

The DTOs are checked against live responses by hand: paste a JWT into `ACCESS_TOKEN` at the top of
`tests/integration_test.py`, then either `uv run pytest tests/integration_test.py` (it skips while
the token is empty) or `uv run python tests/integration_test.py`. It calls every wrapped endpoint
once and reports, per endpoint, anything it could not decode, any key no model declares, and the
declared fields the payload left out.

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

### The write endpoints are not wrapped

Placing, amending and cancelling an order (4.1–4.3 and 6.4/6.5/6.8/6.9/6.10/6.11) and moving
cash between accounts or into and out of margin (3.1–3.3) are not part of this library, so
every function it exposes only reads. `get_token` is the sole `POST`, and it only exchanges
the API key for a token. Call those endpoints directly with `requests` if you need them.

The derivatives endpoints are not wrapped at all — none of section 6 or 7.1.

Seven further read operations were never wrapped, so they are missing too: 4.10 margin quota,
4.11 risk and margin ratios, 4.12 supplementary loan package, 4.13 loan list, 4.17 debt
lookup, 4.18 margin pricing policy, and the REST `/api/v1/derivatives/contracts` price board.
That leaves 19 of the 44 operations covered.

### The models follow live responses where the document is wrong

Every DTO field starts from `openapi-v1.0.0.json` for the operation that returns it, but the
document is wrong, thin or silent often enough that fifteen of the nineteen operations were
corrected against real payloads — `tests/integration_test.py` is what keeps this honest:

<!-- The table below is included by docs/limitations.md, so edit it here only. -->
<!-- --8<-- [start:drift-table] -->
| Op | The document says | The endpoint actually sends |
| --- | --- | --- |
| 2.1 | `basicInfo`, `bankSubAccounts` | plus `personalInfo` (with `identityCard`), `personalBasicInfo`, `accountStatus`, `bankAccounts`, `systemUserInfo`, `rmRefInfo` |
| 4.4 | rows under `orders` | rows under `data`, beside an `object`/`totalCount`/`pageSize`/`pageIndex` header |
| 4.6 | page fields | the same, plus `object` |
| 4.7 | `purchasingPower`, `maxQuantity` | the 16-field `ppse` object |
| 4.8, 4.9 | `pp0`, `maxQtty` | the same 16-field `ppse` object, so all three share `PurchasingPowerResponse` |
| 4.14 | `assets` records of 4 fields | `stock` records of 32 fields |
| 4.15 | 5 fields | the whole 32-field record, with `fullName` as the *string* `"null"` |
| 4.16 | query parameter `accountno`, full page header | `acctno`, and a page of just `{"data": []}` when nothing matches |
| 5.1 | prices and totals always present | adds `nextCeilPrice`/`nextFloorPrice`/`nextRefPrice`, omits most fields outside trading hours, so only `symbol` is required |
| 5.3 | 13 row fields and a `tradingDate` | 28 keys, no `tradingDate`, every number quoted, and `buyForeignQtty`/`change`/`room`/`bidPrice03` absent on some symbols |
| 5.4 | match rows of five fields | match rows also carry `color` |
| 5.5 | 8 row fields | 15 keys, including `rcp`/`pcp`, the trading date `d` and five nulls that stay `Any` |
| 5.7 | `ticker`, `data` | plus an undocumented `d` |
| 5.11 | no response at all | a page of `content` rows, each with a 36-field `securitiesInfo` block, and `pageable`/`sort` |
<!-- --8<-- [end:drift-table] -->

Where a payload showed a field can be absent, that field is optional rather than required, and
fields whose JSON type no live value pinned down stay `Any` — `avatarData`, `personalBasicInfo`, an
`rmRefInfo` item, 5.5's `pcps`/`hc`/`ac`/`pcpc` and `as_`, 5.3's `sellForeignQtty`, 5.4's `color`
and 5.7's `d`. 5.5's `as` is a Python keyword, so that field is `as_` — see the alias note below.
5.11's models describe the full `fields=all` projection, so a narrower `fields` raises a
`ValidationError` naming what is missing.

Two things follow:

- **Unknown keys are ignored, omitted ones default.** A field TCBS leaves out falls back to its
  default, so `orders`, `data`, `stock`, `response` and friends are `None` when the API omits
  them — as long as the model declares them optional.
- **Annotations say what a value means, and pydantic coerces in lax mode.** `"30500"` lands in
  a `float` field as `30500.0`, which is how 5.3's quoted prices and 5.11's `newPrice` read as
  numbers; anything that may be fractional is a `float` rather than an `int` for the same
  reason.

### Every field is described

All 437 fields on these models carry a `Field(description=...)`, so `model_json_schema()` — and
any documentation generated from it — explains the payload. The text comes from the OpenAPI
document where the document has it; from 5.11's own documentation page, whose response table is
hand-written precisely because the document declares none; and from the captured payloads
otherwise. A field nothing explains says so instead of guessing: 5.5's `rcp`/`pcp`, 5.4's `color`,
5.7's `d`, the five `Any` fields 5.5 sends as null, and the 4.14/4.15 counters whose meaning only
TCBS knows.

### When a payload does not fit

`request_api.decode` is a thin `model_validate`, so a response that does not match its model —
a required field missing, a value that cannot be coerced — raises pydantic's `ValidationError`
rather than handing back a half-built object:

```python
from pydantic import ValidationError

from tcbs_api.service import market as market_service

try:
    response = market_service.get_foreign_room(token, index=1)
except ValidationError as exc:
    print(exc.errors())  # [{'loc': ('data', 0, 'matchPrice'), 'msg': 'Input should be a valid number', ...}]
```

Fields the API sends that the model does not declare are ignored, so a new column never breaks a
call; a *changed* type or a missing required field is worth reporting upstream. To get the
payload back out of a model, dump it:

```python
response.model_dump()  # field names
response.model_dump(by_alias=True)  # JSON keys — "as" rather than "as_"
```

### A response key that is not a legal Python name

5.5's `as` key is a Python keyword, so the field is `as_` and carries the JSON spelling as a
pydantic alias:

```python
from typing import Any

from pydantic import Field

as_: Any = Field(default=None, alias="as")
```

Every model sets `populate_by_name`, so `row.as_` and `Row(as_=…)` work as well as the payload's
`as` key, and `model_dump(by_alias=True)` writes `as` back out.

### Operational notes

- The token endpoint is limited to **10 requests per day** by TCBS; cache the token.
- The library performs no retries, rate limiting, or token refresh — callers own that
  policy.
- Requests are issued synchronously with `requests`. There is no async client.

## License

MIT — see [LICENSE](https://github.com/nghialuffy/tcbs-api/blob/main/LICENSE).

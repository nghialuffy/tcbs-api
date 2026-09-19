# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v1.0.0.html).

## [0.0.2] - 2026-09-20

### Added

- **Cash-market data (5.x).** New `tcbs_api.service.market` and `tcbs_api.dto.market`
  modules wrapping eight market-data endpoints: `get_symbol_and_price` (5.1),
  `get_foreign_room` (5.3), `get_put_through` (5.4), `get_price_matching_history` (5.5),
  `get_supply_demand_intraday` (5.6), `get_supply_demand_daily` (5.7),
  `get_supply_demand_monthly` (5.8) and `get_securities_info` (5.11). Each function's
  docstring links its TCBS documentation page.
- **Cash statement (4.16).** `stock_normal.get_cash_statement` wraps
  `GET /erebos/v2/digital/trans-hist-cashStatements`, modelled by `CashStatementResponse`,
  `CashStatementPage` and `CashStatementDetail`.
- Market-data functions take `token` first and their optional filters as keyword-only
  arguments, since none of those filters can precede a required `token`; the rest of the
  library keeps `token` as its last positional argument. A `None` filter is omitted from
  the query string.
- Coverage is now 37 of the 44 operations in the TCBS OpenAPI document. Still missing:
  4.10 margin quota, 4.11 risk and margin ratios, 4.12 supplementary loan package,
  4.13 loan list, 4.17 debt lookup, 4.18 margin pricing policy, and the REST
  `/api/v1/derivatives/contracts` price board.

## [0.0.1] - 2026-09-19

### Changed

- **Repackaged for distribution.** The project is now a standard, PEP 517/518
  installable package that works with `uv`, `pip`, and any other standards-compliant
  installer.
- **Import package renamed** from the generic top-level `openapi` to `tcbs_api`, so it
  matches the distribution name `tcbs-api` and no longer risks colliding with another
  package on `sys.path`. Every public import changes accordingly, for example
  `import openapi.service.stock_normal.normal` becomes
  `from tcbs_api.service.stock_normal import normal`.
- Replaced `setup.py` with a declarative `pyproject.toml` (hatchling build backend) and
  a single-sourced `__version__` in `tcbs_api/__init__.py`.
- Trimmed `install_requires` from a 65-entry `pip freeze` dump down to the three
  packages actually imported: `requests`, `dacite`, and `dataclasses-json`.
- Moved the commented-out usage demo out of the installed package and into the README.
- Package metadata now credits **nghialuffy** as the author and points at the GitHub
  repository: `Homepage`, `Repository`, `Issues`, and `Changelog` URLs were added, and the
  TCBS documentation site moved to the `Documentation` URL. The MIT `LICENSE` copyright
  holder was updated to match.
- The 28 doc-comment links in the service modules were repointed at the current
  `https://developers.tcbs.com.vn/docs/v1.0.0/…` documentation. The Redoc-style
  `#tag/…/operation/…` anchors they pointed at no longer exist.
- License metadata now uses the PEP 639 SPDX form — `license = "MIT"` plus
  `license-files = ["LICENSE"]`, which publishes `License-Expression: MIT` — and the
  `License :: OSI Approved :: MIT License` classifier was dropped, because PEP 639 forbids
  combining a license classifier with a `License-Expression`.

### Fixed

- **`from .money import *` shadowed the money service module.** Because
  `tcbs_api/service/money/money.py` imports the DTO module as `money`, the wildcard
  re-export in its `__init__.py` rebound the `money` attribute to the DTO module. As a
  result both `from tcbs_api.service.money import money` and
  `import tcbs_api.service.money.money as money_service` — the form the old README
  documented — resolved to `tcbs_api.dto.money.money`, so
  `money_service.transfer_between_subaccounts(...)` raised `AttributeError`.
  `tcbs_api/service/money/__init__.py` is the one package that now lists its three
  functions explicitly. Every other package keeps its wildcard re-export, so those
  packages continue to leak their imports (`requests`, `Config`, `constant`, …) into
  their namespaces.
- **`get_command_match_information` called the wrong endpoint.** It requested
  `/aion/v1/accounts/{accountNo}/orders` — the same URL as `get_orders`, decoding a
  different response DTO. The documented `get order matching information` operation is
  `GET /aion/v1/accounts/{accountNo}/matching-details`, whose response fields
  (`orderId`, `side`, `symbol`, `quoteQtty`, `quotePrice`, `tradeId`, `qtty`, `price`,
  `timeExec`) match `CommandMatchInformationDetailResponse` exactly.
- **Four DTO classes could not be instantiated.** `OrderConditionDerivativeResponseDTO`,
  `EditOrderNormalDerivativeResponseDTO`, `EditOrderConditionDerivativeResponseDTO`, and
  `CancelOrderNormalDerivativeResponseDTO` had `@dataclass` above `@dataclass_json`
  instead of below it. That order leaves `__init__` set to `object.__init__`, so the
  classes raised `TypeError: takes no arguments` on construction and on `from_json()`.
  The decorator order now matches the other DTOs in the module.

### Removed

- Committed build artifacts: `open_api_tcbs.egg-info/`, `PKG-INFO`, `setup.cfg`,
  `SOURCES.txt`, `requires.txt`, and `top_level.txt`.
- The shadowed duplicate `OrderConditionDerivativeRequestDTO` definition in
  `tcbs_api/dto/derivative_dto/derivative_dto.py` (the first had `str` fields and was
  overwritten by the second, which is the signature the documented call site uses).
- Unused `Optional`/`field` imports in `tcbs_api/dto/money/money.py`.
- **All `print()` calls in the service layer.** A stray `print(response)` in
  `get_token()` wrote a raw `requests.Response` to stdout on every call, and 11
  `print(response.json())` calls ran on the error path. The latter executed *before*
  `raise_for_status()`, so a non-JSON error body (a proxy 502, an HTML error page) raised
  `JSONDecodeError` from `json()` and masked the `requests.HTTPError` the README
  documents; they also wrote response payloads to stdout. Errors now surface solely as
  `requests.HTTPError`, whose `response` attribute carries the body.

### Added

- `LICENSE` (MIT), this changelog, and a `.gitignore`.
- `tcbs_api/py.typed` (PEP 561) so type checkers use the inline DTO annotations.
- `ruff` and `mypy` configuration in `pyproject.toml`.
- Type annotations across the public service and utility API.
- `.github/workflows/publish.yml`, which publishes to PyPI via OIDC trusted publishing
  (no API token in the repo), gated on `twine check --strict` and a tag/version match,
  plus a "Releasing" section in the README covering the one-time PyPI setup.

# Quick start

Everything goes through one token, fetched once, then passed as the last positional argument to
every call.

```python
from tcbs_api.service import account as account_service, token as token_service

API_KEY = "your-api-key"
OTP = "your-otp"

token = token_service.get_token(API_KEY, OTP).token
```

!!! warning "The token endpoint allows 10 requests per day"

    TCBS rate limits operation 1.1 to **10 requests per day**. Fetch the token once, persist it,
    and reuse it — calling `get_token` on every request will lock you out until the next day.
    The library does not cache or refresh the token for you.

## 1. Exchange the API key for a token

```python
from tcbs_api.service import token as token_service

response = token_service.get_token(API_KEY, OTP)
print(response.token)
```

This is the only unauthenticated endpoint, and the only one that sends a `POST`. The call
returns a [`TokenResponseDto`](../api/models.md#tcbs_api.dto.token) whose `token` is the JWT every other
function needs.

## 2. Read account information

```python
from tcbs_api.service import account as account_service

custody_code = "0001201435"
info = account_service.get_subaccount_info(
    custody_code,
    "basicInfo,personalInfo:fullName,bankSubAccounts",
    token,
)
print(info.bankSubAccounts[0].accountNo, info.basicInfo.tcbsId, info.personalInfo.fullName)
```

The second argument is the `fields` parameter: a comma-separated list of the profile blocks to
return. Blocks you leave out come back as `None`, and appending `:field` (as in
`personalInfo:fullName`) narrows a block to a single field. Passing an empty string asks for
every block. See [Account information](../guides/account-information.md).

## 3. Read holdings and cash

```python
from tcbs_api.service import stock as stock_service

holdings = stock_service.get_asset_stock_by_sub_account("0001F77149", token)
for holding in holdings.stock:
    print(holding.symbol, holding.availableTrading, holding.currentPrice, holding.totalQtty)

cash = stock_service.get_cash_investment("0001F77149", token)
print(cash.data[0].balance, cash.data[0].pp0, cash.data[0].blockAmountInfo.blockAmountTotal)
```

See [Holdings and cash](../guides/holdings-and-cash.md).

## 4. Read market data

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

The board endpoints carry prices in VND; see [Market data](../guides/market-data.md) for the
basket codes, the investor classes and the endpoints that come with caveats.

## Argument order

Two call shapes, and the rule is: **`token` is a positional argument unless every other
argument is an optional filter.**

- Where the endpoint has a required argument of its own — a symbol, an account number — that
  argument comes first and `token` comes last, as in
  `get_supply_demand_daily("FPT", token, investor_type="shark")`.
- Where everything except the token is an optional filter, `token` comes first and the filters
  are keyword-only, as in `get_symbol_and_price(token, index=1)`.

Filters left as `None` never reach the query string, which is what `requests` does with a
`None` value.

## Next

- [Account information](../guides/account-information.md)
- [Holdings and cash](../guides/holdings-and-cash.md)
- [Market data](../guides/market-data.md)
- [Errors and validation](../guides/errors-and-validation.md)

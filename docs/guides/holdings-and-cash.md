# Holdings and cash

The 4.x stock endpoints are all under
[`tcbs_api.service.stock`](../api/services.md#tcbs_api.service.stock), and all take an account number before the
token.

```python
from tcbs_api.service import stock as stock_service
```

`account_no` is the **sub-account** number, not the custody account: `0001A23456` rather than
`0001C23456`. List a custody account's sub-accounts with `get_subaccount_info(...,
"bankSubAccounts", token)` — see [Account information](account-information.md).

## The order book

```python
orders = stock_service.get_orders("0001A23456", token)
for order in orders.data or []:
    print(order.orderId, order.symbol, order.execType, order.status, order.price, order.quantity)
```

`data` is the page of [`OrderSummary`](../api/models.md#tcbs_api.dto.stock) rows, beside the
`object`/`totalCount`/`pageSize`/`pageIndex` header. Note the field name: the OpenAPI document
calls those rows `orders`, the endpoint actually sends them under `data`.

A single order, by the id from that page:

```python
order = stock_service.get_order("0001A23456", order_id="123456", token=token)
print(order.data[0].matchPrice, order.data[0].orStatus)
```

And the trades that have matched, with their fees and taxes:

```python
matches = stock_service.get_command_match_information("0001A23456", token)
```

## Purchasing power

Three endpoints answer the same `ppse` object — the plain one, one for a symbol, and one for a
symbol at a price:

```python
pp = stock_service.get_purchasing_power("0001A23456", token)
print(pp.pp0, pp.availableTrade, pp.maxBuyQuantity)

pp_fpt = stock_service.get_purchasing_power_by_symbol("0001A23456", "FPT", token)
pp_fpt_at_30 = stock_service.get_purchasing_power_by_symbol_and_price("0001A23456", "FPT", 30.0, token)
```

`pp0` is the only field the API document describes — the basic purchasing power. `ppse` is the
figure for the symbol the check was run at; `availableTrade`, `ppseref`, `realMaxBuyQuantity` and
`minBuyQuantity` are undocumented extras the live payload carries. In particular
`minBuyQuantity` is **not** the exchange's round-lot rule: on HOSE a lot is 100 shares, and this
value does not change with price, so do not read an order size out of it. Every field is optional,
because the endpoint omits the ones that do not apply. The OpenAPI document describes these
responses as a handful of fields; the live payload is the 16-field object the model follows — see
[Known limitations](../limitations.md#the-models-follow-live-responses-where-the-document-is-wrong).

## Holdings

```python
assets = stock_service.get_asset_stock_by_sub_account("0001A23456", token)
for holding in assets.stock or []:
    print(
        holding.symbol,
        holding.totalQtty,  # total shares held
        holding.availableTrading,  # shares that can be sold today
        holding.currentPrice,
        holding.costPrice,
    )
```

`stock` holds one 32-field [`StockAsset`](../api/models.md#tcbs_api.dto.stock) per symbol. The quantities worth
knowing:

| Field | Means |
| --- | --- |
| `totalQtty` | Everything held |
| `availableTrading` | Sellable today |
| `t0` / `t1` / `t2` | Bought today / yesterday / two days ago, still settling |
| `mortgaged`, `securedQuantity` | Pledged against something |
| `stockDividend`, `cashDividend` | Corporate action pending |
| `waitForTrade`, `waitForTransfer`, `waitForWithdraw` | In transit |

## Cash

```python
cash = stock_service.get_cash_investment("0001A23456", token)
record = cash.data[0]

print(record.bodBalance)  # cash actually at TCBS (cashBalance mirrors it)
print(record.bankAvlBalance)  # cash at the IA partner — another layer, not a loan
print(record.balance)  # in transit: may be NEGATIVE, and negative is not an overdraft
print(record.pp0)  # basic purchasing power, across every cash layer
print(record.avlWithdraw)  # withdrawable
print(record.blockAmountInfo.blockAmountTotal)  # blocked, in total

for line in record.blockAmountInfo.details or []:
    print(line.blockType, line.blockAmt)  # blocked, and why
```

`data` carries one record per sub-account. The money sits in four layers, and reading them as a
single figure is the usual way to get the balance wrong:

| Layer | Fields | Read it as |
| --- | --- | --- |
| Cash at TCBS | `bodBalance`, `cashBalance` | Money actually in the sub-account |
| Cash at the IA partner | `bankAvlBalance`, `iaInfos[].available` | Real money held at the partner (e.g. TCB) |
| In transit | `balance` | Unsettled sells and pending settlement. **May be negative — that is money moving, not an overdraft, and not spendable cash** |
| Committed | `buyingAmount`, `secureAmtPO`, the `*BlockAmount` counters | Earmarked for pending orders, still the account's money |

`pp0` is what can be spent across those layers, and it is **not** a margin figure: `pp0` above
`bodBalance` means IA-partner cash or receivables, not leverage. Two spellings come straight from
TCBS and are kept: `pp0forBF`/`pp0ForBond`, and the typos `cashDevident` and
`avalBondBlockAmount`. `fullName` arrives as the four-character string `"null"` rather than JSON
null, so it is typed `str`.

## Cash statement

The transaction history needs six query parameters, all of which TCBS requires:

```python
statement = stock_service.get_cash_statement(
    "0001A23456",
    from_date="2026-09-01",
    to_date="2026-09-30",
    transaction_code="1153",  # "ứng trước tiền bán"; an empty code is rejected
    token=token,
    page_size=10,
    page_index=0,
)

page = statement.response
for line in page.data or []:
    print(line.transactionDate, line.transactionCode, line.transactionName, line.creditAmount, line.debitAmount)
print(page.totalCreditAmount, page.totalDebitAmount)
```

Two things are easy to get wrong here:

- The sub-account goes in the query parameter `acctno`. The OpenAPI document calls it
  `accountno`, but the endpoint does not answer to that name.
- `page_index` is 1-based in TCBS's own sample. When nothing matches, the endpoint answers
  `{"response": {"data": []}}` — no page number and no totals — so every scalar on the page is
  optional and only `data` is worth touching.

The page is nested one level down in `statement.response`, which is why the model has a single
field.

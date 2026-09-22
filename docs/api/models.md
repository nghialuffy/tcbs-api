# Models

Request and response models, grouped by the same domains as the [services](services.md). They
all inherit from `DtoModel` — pydantic v2 models that ignore unknown keys and fill omitted
fields from their defaults.

Field names keep TCBS's camelCase spelling rather than Python's usual snake_case, so
`OrderDetail.orderID` and `CashInvestmentInfo.pp0forBF` are spelled the way the API spells them
and code maps onto payloads directly. A key that is not a legal Python name carries its JSON
spelling as an alias — 5.5's `as_`. Every field carries a description, and that is what the
reference below prints beside it.

::: tcbs_api.dto

::: tcbs_api.dto.base

::: tcbs_api.dto.token

::: tcbs_api.dto.account

::: tcbs_api.dto.stock

::: tcbs_api.dto.market

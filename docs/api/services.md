# Services

One module per API domain, one function per endpoint. Every function is a thin declaration of
one operation — its URL, HTTP verb, query parameters and response model — with the request
plumbing in [Support](support.md).

!!! note "`token` is the last positional argument"

    Unless every other argument is an optional filter, in which case it comes first and the
    filters are keyword-only. Filters left as `None` never reach the query string.

::: tcbs_api.service.token

::: tcbs_api.service.account

::: tcbs_api.service.stock

::: tcbs_api.service.market

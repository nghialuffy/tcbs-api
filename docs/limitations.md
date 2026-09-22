# Known limitations

Three things are worth knowing before you rely on this library: what it deliberately does not
wrap, how far its models follow the OpenAPI document, and what it leaves to the caller.

## The write endpoints are not wrapped

Placing, amending and cancelling an order (4.1–4.3 and 6.4/6.5/6.8/6.9/6.10/6.11) and moving cash
between accounts or into and out of margin (3.1–3.3) are not part of this library, so **every
function it exposes only reads**. `get_token` is the sole `POST`, and it only exchanges the API
key for a token. Call those endpoints directly with `requests` if you need them.

The derivatives endpoints are not wrapped at all — none of section 6, nor 7.1.

Seven further read operations were never wrapped, so they are missing too:

| Operation | |
| --- | --- |
| 4.10 | Margin quota |
| 4.11 | Risk and margin ratios |
| 4.12 | Supplementary loan package |
| 4.13 | Loan list |
| 4.17 | Debt lookup |
| 4.18 | Margin pricing policy |
| — | REST `/api/v1/derivatives/contracts` price board |

That leaves 19 of the 44 operations covered. The [API reference](api/index.md) lists exactly
the ones that are.

## The models follow live responses where the document is wrong

Every DTO field starts from TCBS's OpenAPI document for the operation that returns it, but the
document is wrong, thin or silent often enough that fifteen of the nineteen operations were
corrected against real payloads — the project's integration test is what keeps this honest.
Where they disagree, the payload wins. The table is the same one the README carries, included
from it so the two cannot drift:

--8<-- "README.md:drift-table"

Where a payload showed a field can be absent, that field is optional rather than required, and
fields whose JSON type no live value pinned down stay `Any`. Two consequences:

- **Unknown keys are ignored, omitted ones default.** A field TCBS leaves out falls back to its
  default, so `orders`, `data`, `stock`, `response` and friends are `None` when the API omits
  them — as long as the model declares them optional. See
  [What is tolerated](guides/errors-and-validation.md#what-is-tolerated).
- **Annotations say what a value means, and pydantic coerces in lax mode.** `"30500"` lands in a
  `float` field as `30500.0`, which is how 5.3's quoted prices and 5.11's `newPrice` read as
  numbers; anything that may be fractional is a `float` rather than an `int` for the same reason.

A few payloads stay deliberately raw, because nothing pinned their shape down:
`avatarData`, `personalBasicInfo`, an `rmRefInfo` item, and the `Any`-typed fields listed in
[What is tolerated](guides/errors-and-validation.md#what-is-tolerated).

### Every field is described

All 437 fields on these models carry a `Field(description=...)`, so `model_json_schema()` — and
this documentation, which is generated from it — explains the payload. The text comes from the
OpenAPI document where the document has it; from 5.11's own documentation page, whose response
table is hand-written precisely because the document declares none; and from the captured
payloads otherwise. A field nothing explains says so instead of guessing: 5.5's `rcp`/`pcp`,
5.4's `color`, 5.7's `d`, the five `Any` fields 5.5 sends as null, and the 4.14/4.15 counters
whose meaning only TCBS knows.

## Operational notes

- The token endpoint is limited to **10 requests per day** by TCBS; cache the token. See
  [Quick start](getting-started/quickstart.md#1-exchange-the-api-key-for-a-token).
- The library performs no retries, rate limiting, or token refresh — callers own that policy.
- Requests are issued synchronously with `requests`. There is no async client.
- Market data reflects what the REST snapshot returns; the streaming price board (5.2) is a
  WebSocket and is out of scope.

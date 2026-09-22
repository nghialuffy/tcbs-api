"""The base class every model in this package inherits from.

The models are pydantic v2 models rather than dataclasses, so a response parses with coercion
and unknown keys are ignored. A payload that does not fit raises pydantic's ``ValidationError``
— see `tcbs_api.utils.request_api.decode`.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class DtoModel(BaseModel):
    """Base of every TCBS response model.

    ``extra="ignore"`` because TCBS sends fields this library does not model, and
    ``populate_by_name`` so a field can be read by its Python name *and* by the JSON key it
    aliases — ``PriceMatchingInfo``'s ``as_`` is the only one so far, since ``as`` cannot be a
    field name.

    Validation stays pydantic's default lax mode on purpose: ``"30500"`` becomes ``30500.0``
    for a ``float`` field, which is what the quoted prices of 5.3 and 4.14 need.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


__all__ = ["DtoModel"]

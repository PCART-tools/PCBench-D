def masked_fill(g, self, mask, value):
    mask = _cast_Bool(g, mask, False)  # type: ignore[name-defined]
    value = sym_help._maybe_get_scalar(value)
    return g.op("Where", mask, sym_help._if_scalar_type_as(g, value, self), self)

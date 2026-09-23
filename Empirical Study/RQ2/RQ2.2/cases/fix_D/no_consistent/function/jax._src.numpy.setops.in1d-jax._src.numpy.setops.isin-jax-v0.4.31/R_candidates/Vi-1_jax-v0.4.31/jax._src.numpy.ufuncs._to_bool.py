def _to_bool(x: Array) -> Array:
  return x if x.dtype == bool else lax.ne(x, _lax_const(x, 0))

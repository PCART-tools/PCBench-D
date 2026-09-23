@implements(getattr(np, "unique_values", None))
def unique_values(x: ArrayLike, /) -> Array:
  check_arraylike("unique_values", x)
  return cast(Array, unique(x, equal_nan=False))

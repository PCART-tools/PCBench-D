@implements(getattr(np, "unique_inverse", None))
def unique_inverse(x: ArrayLike, /) -> _UniqueInverseResult:
  check_arraylike("unique_inverse", x)
  values, inverse_indices = unique(x, return_inverse=True, equal_nan=False)
  return _UniqueInverseResult(values=values, inverse_indices=inverse_indices)

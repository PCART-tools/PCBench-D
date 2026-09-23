@implements(getattr(np, "unique_all", None))
def unique_all(x: ArrayLike, /) -> _UniqueAllResult:
  check_arraylike("unique_all", x)
  values, indices, inverse_indices, counts = unique(
    x, return_index=True, return_inverse=True, return_counts=True, equal_nan=False)
  return _UniqueAllResult(values=values, indices=indices, inverse_indices=inverse_indices, counts=counts)

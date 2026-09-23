@implements(getattr(np, "unique_counts", None))
def unique_counts(x: ArrayLike, /) -> _UniqueCountsResult:
  check_arraylike("unique_counts", x)
  values, counts = unique(x, return_counts=True, equal_nan=False)
  return _UniqueCountsResult(values=values, counts=counts)

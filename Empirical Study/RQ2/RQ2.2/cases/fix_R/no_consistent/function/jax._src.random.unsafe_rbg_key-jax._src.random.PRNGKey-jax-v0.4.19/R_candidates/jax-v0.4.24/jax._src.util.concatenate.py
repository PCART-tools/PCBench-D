def concatenate(xs: Iterable[Sequence[T]]) -> list[T]:
  """Concatenates/flattens a list of lists."""
  return list(it.chain.from_iterable(xs))

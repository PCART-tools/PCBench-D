def ref_set(ref: AbstractRef, idx: Indexer, value: Array) -> None:
  """Sets a `Ref`'s value, a.k.a. ref[idx] <- value."""
  ref_swap(ref, idx, value)

def ref_set(ref_or_view: AbstractRef | RefView, idx: Indexer | None, value: Array) -> None:
  """Sets a `Ref`'s value, a.k.a. ref[idx] <- value."""
  ref_swap(ref_or_view, idx, value, _function_name="ref_set")

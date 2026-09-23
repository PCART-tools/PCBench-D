def ref_swap(ref: AbstractRef, idx: Indexer, value: Array) -> Array:
  """Sets a `Ref`'s value and returns the original value."""
  ref_aval = core.get_aval(ref)
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"Can only call `swap` on a `Ref`: {ref}")
  non_slice_idx, indexed_dims = _get_indexer(ref, idx)
  return swap_p.bind(ref, value, *non_slice_idx, indexed_dims=indexed_dims)

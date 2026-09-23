def ref_get(ref: Any, idx: Indexer) -> Array:
  """Reads a value from a `Ref`, a.k.a. value <- ref[idx]."""
  ref_aval = core.get_aval(ref)
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"Can only call `get` on a `Ref`: {ref}")
  non_slice_idx, indexed_dims = _get_indexer(ref, idx)
  return get_p.bind(ref, *non_slice_idx, indexed_dims=indexed_dims)

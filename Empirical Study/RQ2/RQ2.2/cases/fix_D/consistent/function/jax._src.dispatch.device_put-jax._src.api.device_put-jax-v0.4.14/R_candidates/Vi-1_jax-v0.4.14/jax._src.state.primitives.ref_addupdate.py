def ref_addupdate(ref: AbstractRef, idx: Indexer, x: Array) -> None:
  """Mutates a ref with an additive update i.e. `ref[idx] += x`."""
  ref_aval = core.get_aval(ref)
  if not isinstance(ref_aval, AbstractRef):
    raise ValueError(f"Can only call `addupdate` on a `Ref`: {ref}")
  non_slice_idx, indexed_dims = _get_indexer(ref, idx)
  return addupdate_p.bind(ref, x, *non_slice_idx, indexed_dims=indexed_dims)

def _get_indexer(ref: AbstractRef, idx: Indexer
                ) -> Tuple[Indexer, Tuple[bool, ...]]:
  if isinstance(ref.inner_aval, core.ShapedArray):
    non_slice_idx, indexed_dims = _unpack_idx(idx, ref.ndim)
  else:
    if not _is_trivial_indexer(idx):
      raise ValueError(
          f"Cannot use nontrivial slice on non-shaped `Ref`: {idx}.")
    non_slice_idx, indexed_dims = (), ()
  return non_slice_idx, indexed_dims

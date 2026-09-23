def _get_lowering_rule(
    ctx: TritonLoweringRuleContext, ptr, *non_slice_idx, indexed_dims
):
  ref_block_info, *_ = ctx.block_infos
  idx = _pack_indices(non_slice_idx, indexed_dims)
  avals_in = ctx.avals_in
  idx_avals = _pack_indices(avals_in[1:], indexed_dims)
  if not isinstance(ptr.type, tl.pointer_type):
    assert len(avals_in) == 1
    return ptr
  if non_slice_idx:
    (int_indexer_shape,) = {
        i.shape for i in idx_avals if not isinstance(i, slice)
    }
  else:
    int_indexer_shape = ()
  idx = tuple(
      primitives.Slice.from_slice(slc, s) if isinstance(slc, slice) else slc
      for s, slc in zip(avals_in[0].shape, idx)
  )
  idx = primitives.NDIndexer(idx, avals_in[0].shape, int_indexer_shape)
  ptr = _compute_pointers_from_indices(
      ptr, ref_block_info, idx, avals_in[0].shape, ctx.builder
  )
  return tl.load(ptr, _builder=ctx.builder)

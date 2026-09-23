def _swap_lowering_rule(
    ctx: TritonLoweringRuleContext, ptr, value, *non_slice_idx, indexed_dims
):
  ref_block_info, *_ = ctx.block_infos
  avals_in = ctx.avals_in
  idx = _pack_indices(non_slice_idx, indexed_dims)
  idx_avals = _pack_indices(avals_in[2:], indexed_dims)
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
  mask = None
  old_value = tl.load(ptr, mask=mask, _builder=ctx.builder)
  tl.store(ptr, value, mask=mask, _builder=ctx.builder)
  return old_value

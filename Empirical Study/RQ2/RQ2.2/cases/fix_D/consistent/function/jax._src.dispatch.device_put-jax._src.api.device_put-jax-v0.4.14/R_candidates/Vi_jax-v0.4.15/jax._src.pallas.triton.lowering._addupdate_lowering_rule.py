def _addupdate_lowering_rule(
    ctx: TritonLoweringRuleContext, ptr, value, *non_slice_idx, indexed_dims
):
  ref_block_info, *_ = ctx.block_infos
  avals_in = ctx.avals_in
  idx = _pack_indices(non_slice_idx, indexed_dims)
  if non_slice_idx:
    (int_indexer_shape,) = {
        tuple(map(lambda x: x.value, i.shape)) for i in non_slice_idx
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
  tl.atomic_add(ptr, value, _builder=ctx.builder)
  return []

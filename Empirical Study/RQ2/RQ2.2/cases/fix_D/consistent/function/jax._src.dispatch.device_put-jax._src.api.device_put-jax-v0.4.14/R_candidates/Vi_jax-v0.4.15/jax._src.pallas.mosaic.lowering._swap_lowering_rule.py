def _swap_lowering_rule(
    ctx: LoweringRuleContext,
    ref,
    val,
    *non_slice_idx,
    indexed_dims: Sequence[bool],
):
  # Call _masked_swap_lowering_rule (since it's more general)
  ref_aval, val_aval, *non_slice_idx_avals = ctx.avals_in
  nd_indexer, nd_indexer_avals = _convert_flat_indexing_to_indexer(
      ref_aval, non_slice_idx, non_slice_idx_avals, indexed_dims)
  flat_args, tree = tree_util.tree_flatten((nd_indexer,))
  flat_avals = tree_util.tree_leaves((nd_indexer_avals,))
  ctx = ctx.replace(avals_in=(ref_aval, val_aval, *flat_avals))
  return _masked_swap_lowering_rule(ctx, ref, val, *flat_args, args_tree=tree,
                                    masked=False)

def _get_lowering_rule(
    ctx: LoweringRuleContext, ref, *non_slice_idx, indexed_dims: Sequence[bool]
):
  # Call _load_lowering_rule (since it's more general)
  ref_aval, *non_slice_idx_avals = ctx.avals_in
  nd_indexer, nd_indexer_avals = _convert_flat_indexing_to_indexer(
      ref_aval, non_slice_idx, non_slice_idx_avals, indexed_dims)
  flat_args, tree = tree_util.tree_flatten((nd_indexer,))
  flat_avals = tree_util.tree_leaves((nd_indexer_avals,))
  ctx = ctx.replace(avals_in=(ref_aval, *flat_avals))
  return _load_lowering_rule(ctx, ref, *flat_args, args_tree=tree,
                             masked=False)

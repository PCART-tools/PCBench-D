def _addupdate_lowering_rule(
    ctx: TritonLoweringRuleContext, ptr, value, *idx, tree
):
  indexers = tree_util.tree_unflatten(tree, idx)
  if not isinstance(ptr.type, tc.pointer_type):
    assert len(indexers) == 0
    return ptr
  if len(indexers) > 1:
    raise NotImplementedError("No support for multiple indexers yet.")
  indexer = indexers[0]
  ptr = _compute_pointers_from_indices(
      ptr, ctx.block_infos[0], indexer, ctx.avals_in[0].shape,
  )
  tc.atomic_add(ptr, value)
  return []

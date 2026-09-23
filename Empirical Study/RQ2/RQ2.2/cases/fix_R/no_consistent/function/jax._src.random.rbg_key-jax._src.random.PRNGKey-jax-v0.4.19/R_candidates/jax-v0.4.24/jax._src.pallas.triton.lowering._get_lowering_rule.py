def _get_lowering_rule(
    ctx: TritonLoweringRuleContext, ptr, *idx, tree
):
  indexers = tree_util.tree_unflatten(tree, idx)
  if not isinstance(ptr.type, tc.pointer_type):
    assert len(indexers) == 0
    return ptr
  if len(indexers) > 1:
    raise NotImplementedError("No support for multiple indexers yet.")
  indexer = indexers[0]
  args_flat, args_tree = tree_util.tree_flatten((ptr, (indexer,), None, None))
  return _masked_load_lowering_rule(
      ctx,
      *args_flat,
      args_tree=args_tree,
      eviction_policy=None,
      cache_modifier=None,
      is_volatile=False,
  )

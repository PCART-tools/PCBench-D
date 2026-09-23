def _atomic_lowering_rule(
    ctx: TritonLoweringRuleContext,
    *args_flat,
    args_tree,
    atomic_type: primitives.AtomicOpType,
):
  ptr, indexers, value, mask = args_tree.unflatten(args_flat)
  if len(indexers) != 1:
    raise NotImplementedError("Only single indexer is supported.")
  idx = indexers[0]
  ptr = _compute_pointers_from_indices(
      ptr, ctx.block_infos[0], idx, ctx.avals_in[0].shape
  )
  op = _ATOMIC_OP_MAPPING.get(atomic_type)
  if op is None:
    raise NotImplementedError(atomic_type)
  return op(ptr, value, mask=mask)

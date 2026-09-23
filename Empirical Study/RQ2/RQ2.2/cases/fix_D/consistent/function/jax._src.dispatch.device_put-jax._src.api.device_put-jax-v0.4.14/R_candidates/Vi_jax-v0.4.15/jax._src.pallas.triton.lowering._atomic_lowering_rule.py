def _atomic_lowering_rule(
    ctx: TritonLoweringRuleContext,
    ptr,
    value,
    *args,
    args_tree,
    masked: bool,
    atomic_type: primitives.AtomicOpType
):
  ref_block_info, *_ = ctx.block_infos
  idx, *mask_rest = tree_util.tree_unflatten(args_tree, args)
  avals_in = ctx.avals_in
  ptr = _compute_pointers_from_indices(
      ptr, ref_block_info, idx, avals_in[0].shape, ctx.builder
  )
  mask = None
  if masked:
    assert len(mask_rest) == 1
    (mask,) = mask_rest
  if atomic_type not in _ATOMIC_OP_MAPPING:
    raise NotImplementedError(atomic_type)
  op = _ATOMIC_OP_MAPPING[atomic_type]
  return op(ptr, value, mask=mask, _builder=ctx.builder)

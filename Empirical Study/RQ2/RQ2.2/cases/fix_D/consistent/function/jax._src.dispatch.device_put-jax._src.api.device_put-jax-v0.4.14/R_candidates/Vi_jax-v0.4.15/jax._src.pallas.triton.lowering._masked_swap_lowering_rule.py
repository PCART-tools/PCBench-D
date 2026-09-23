def _masked_swap_lowering_rule(
    ctx: TritonLoweringRuleContext,
    ptr,
    value,
    *args,
    args_tree,
    masked,
    eviction_policy
):
  ptr_type = (
      ptr.type.element_ty.element_ty
      if ptr.type.is_block()
      else ptr.type.element_ty
  )
  value_type = value.type.element_ty if value.type.is_block() else value.type
  assert ptr_type == value_type, (ptr_type, value_type)
  ref_block_info, *_ = ctx.block_infos
  idx, *mask_other = tree_util.tree_unflatten(args_tree, args)
  avals_in = ctx.avals_in
  idx_avals, *_ = tree_util.tree_unflatten(args_tree, avals_in[2:])
  ptr = _compute_pointers_from_indices(
      ptr, ref_block_info, idx, avals_in[0].shape, ctx.builder
  )
  mask = None
  if masked:
    assert len(mask_other) == 1
    (mask,) = mask_other
  return tl.store(ptr, value, mask=mask, _builder=ctx.builder)

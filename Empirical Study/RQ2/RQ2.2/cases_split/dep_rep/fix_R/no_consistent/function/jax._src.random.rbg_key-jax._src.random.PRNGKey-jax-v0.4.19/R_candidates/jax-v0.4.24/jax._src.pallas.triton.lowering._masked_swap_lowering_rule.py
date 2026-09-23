def _masked_swap_lowering_rule(
    ctx: TritonLoweringRuleContext, *args_flat, args_tree, eviction_policy
):
  ptr, indexers, value, mask = args_tree.unflatten(args_flat)
  if len(indexers) > 1:
    raise NotImplementedError("No support for multiple indexers yet.")
  idx = indexers[0]
  ptr_type = (
      ptr.type.element_ty.element_ty
      if ptr.type.is_block()
      else ptr.type.element_ty
  )
  value_type = value.type.element_ty if value.type.is_block() else value.type
  assert ptr_type == value_type, (ptr_type, value_type)
  ptr = _compute_pointers_from_indices(
      ptr, ctx.block_infos[0], idx, ctx.avals_in[0].shape
  )
  other = None
  if value is not None and mask is not None:
    other = tc.broadcast_to(value, mask.shape)
  old_value = tc.load(ptr, mask=mask, other=other)
  tc.store(
      ptr,
      value,
      mask=mask,
      eviction_policy=eviction_policy,
  )
  return old_value

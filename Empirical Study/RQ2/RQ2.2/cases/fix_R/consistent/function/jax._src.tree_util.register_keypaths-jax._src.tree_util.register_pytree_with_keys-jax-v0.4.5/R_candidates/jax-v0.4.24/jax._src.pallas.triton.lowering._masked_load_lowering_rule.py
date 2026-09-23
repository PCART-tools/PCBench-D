def _masked_load_lowering_rule(
    ctx: TritonLoweringRuleContext,
    *args_flat,
    args_tree,
    eviction_policy,
    cache_modifier,
    is_volatile,
):
  ptr, indexers, mask, other = args_tree.unflatten(args_flat)
  if len(indexers) > 1:
    raise NotImplementedError("No support for multiple indexers yet.")
  idx = indexers[0]
  if not isinstance(ptr.type, tc.pointer_type):
    assert len(ctx.avals_in) == 1
    return ptr
  ptr = _compute_pointers_from_indices(
      ptr, ctx.block_infos[0], idx, ctx.avals_in[0].shape
  )
  if other is not None and mask is not None:
    other = tc.broadcast_to(other, mask.shape)
  val = tc.load(
      ptr,
      mask=mask,
      other=other,
      cache_modifier=cache_modifier,
      is_volatile=is_volatile,
      eviction_policy=eviction_policy,
  )
  # `tl.load` of a `*int1` returns a tensor with type `int8`, so fix the type.
  return tc.semantic.cast(val, ptr.dtype.element_ty)

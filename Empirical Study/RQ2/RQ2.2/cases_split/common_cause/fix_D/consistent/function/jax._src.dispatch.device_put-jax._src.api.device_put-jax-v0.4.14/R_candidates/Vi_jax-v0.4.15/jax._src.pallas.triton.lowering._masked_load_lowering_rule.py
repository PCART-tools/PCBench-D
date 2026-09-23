def _masked_load_lowering_rule(
    ctx: TritonLoweringRuleContext,
    ptr,
    *args,
    args_tree,
    masked,
    eviction_policy,
    cache_modifier,
    is_volatile
):
  ref_block_info, *_ = ctx.block_infos
  idx, *mask_other = tree_util.tree_unflatten(args_tree, args)
  avals_in = ctx.avals_in
  if not isinstance(ptr.type, tl.pointer_type):
    assert len(avals_in) == 1
    return ptr
  ptr = _compute_pointers_from_indices(
      ptr, ref_block_info, idx, avals_in[0].shape, ctx.builder
  )
  mask, other = None, None
  if masked:
    assert 0 < len(mask_other) <= 2
    if len(mask_other) == 2:
      mask, other = mask_other
    elif len(mask_other) == 1:
      (mask,) = mask_other
  return tl.load(
      ptr,
      mask=mask,
      other=other,
      cache_modifier=cache_modifier,
      volatile=is_volatile,
      eviction_policy=eviction_policy,
      _builder=ctx.builder,
  )

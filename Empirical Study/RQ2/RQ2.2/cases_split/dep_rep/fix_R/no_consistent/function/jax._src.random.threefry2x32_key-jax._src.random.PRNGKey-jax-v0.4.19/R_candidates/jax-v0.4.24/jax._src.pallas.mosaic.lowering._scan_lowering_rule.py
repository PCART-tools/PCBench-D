def _scan_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    jaxpr: jax_core.Jaxpr,
    linear: tuple[bool, ...],
    length: int,
    reverse: bool,
    unroll: bool,
    num_consts: int,
    num_carry: int,
):
  # Can only handle fori_loop-like scans
  num_extensive = len(args) - num_consts - num_carry
  if num_extensive: raise NotImplementedError
  if reverse: raise NotImplementedError
  del linear, num_extensive, reverse

  jaxpr, jaxpr_consts = jaxpr.jaxpr, jaxpr.consts
  if jaxpr_consts: raise NotImplementedError
  del jaxpr_consts

  jaxpr, has_loop_index = (
      pallas_utils.pattern_match_scan_to_fori_loop(jaxpr, num_consts, num_carry)
      )
  consts, args = split_list(args, [num_consts])
  consts_avals, args_avals = split_list(ctx.avals_in, [num_consts])
  if has_loop_index:
    loop_index_start, *args = args
    args_avals = args_avals[1:]
  else:
    loop_index_start = 0
  consts = map(_ensure_mlir_value, consts, consts_avals)
  args = map(_ensure_mlir_value, args, args_avals)
  out = _lower_jaxpr_to_for_loop(
      ctx, jaxpr, loop_index_start, length,
      consts, *args, has_loop_index=has_loop_index,
      unroll=unroll)
  if has_loop_index:
    out = [ir_constant(length,
                       mlir_type=_dtype_to_ir_type(jnp.dtype('int32'))),
           *out]
  return out

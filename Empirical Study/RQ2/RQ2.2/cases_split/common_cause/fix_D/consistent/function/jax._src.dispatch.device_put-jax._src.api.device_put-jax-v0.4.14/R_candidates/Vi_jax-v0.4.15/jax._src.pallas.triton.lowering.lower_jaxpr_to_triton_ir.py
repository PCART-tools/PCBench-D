def lower_jaxpr_to_triton_ir(
    ctx: TritonModuleContext,
    jaxpr: jax_core.Jaxpr,
    block_infos: Sequence[BlockInfo | None] | None,
    *args
) -> Sequence[Any]:
  env = {}
  block_info_env = {}

  def read_env(var: jax_core.Atom):
    if type(var) is jax_core.Literal:
      t = tl.core._to_tensor(np.array(var.val).tolist(), builder=ctx.builder)
      dst_ty = code_gen.str_to_ty(get_triton_type(var.aval)).element_ty
      if t.type.scalar != dst_ty:
        # _to_tensor(np.array(var.val).tolist()) can be lossy e.g. np.float64
        # comes out of .tolist() as list[float], which then comes out of
        # _to_tensor as a block of f32.
        t = tl.semantic.cast(t, dst_ty, ctx.builder)
      return t
    return env[var]

  def read_block_info_env(var: jax_core.Atom):
    if type(var) is jax_core.Literal:
      return None
    return block_info_env.get(var, None)

  def write_env(var: jax_core.Var, val):
    env[var] = val

  if block_infos is None:
    block_infos = [None] * len(jaxpr.invars)
  for invar, block_info in zip(jaxpr.invars, block_infos):
    block_info_env[invar] = block_info
  map(write_env, jaxpr.invars, args)
  for eqn in jaxpr.eqns:
    invals = map(read_env, eqn.invars)
    if eqn.primitive not in triton_lowering_rules:
      raise NotImplementedError(
          "Unimplemented primitive in Pallas GPU lowering: "
          f"{eqn.primitive.name}. "
          "Please file an issue on https://github.com/google/jax/issues.")
    rule = triton_lowering_rules[eqn.primitive]
    avals_in = [v.aval for v in eqn.invars]
    avals_out = [v.aval for v in eqn.outvars]
    eqn_block_infos = map(read_block_info_env, eqn.invars)
    rule_ctx = TritonLoweringRuleContext(
        ctx, avals_in, avals_out, eqn_block_infos
    )
    try:
      outvals = rule(rule_ctx, *invals, **eqn.params)
    except TritonLoweringException:
      raise  # We only add the extra info to the innermost exception.
    except Exception as e:
      raise TritonLoweringException(
          f"Exception while lowering eqn:\n  {eqn}\n"
          f"With context:\n  {rule_ctx}\n"
          f"With inval shapes={map(lambda t: t.shape, invals)}\n"
          f"With inval types={map(lambda t: t.type, invals)}\n"
          f"In jaxpr:\n{jaxpr}") from e
    if eqn.primitive.multiple_results:
      map(write_env, eqn.outvars, outvals)
    else:
      write_env(eqn.outvars[0], outvals)
  return map(read_env, jaxpr.outvars)

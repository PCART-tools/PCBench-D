def _run_scoped_lowering_rule(ctx: LoweringRuleContext, *consts, jaxpr):
  region = tpu.RegionOp()
  in_avals = [v.aval for v in jaxpr.invars]
  jaxpr = pe.convert_constvars_jaxpr(jaxpr)
  with ir.InsertionPoint(region.body):
    args = map(_alloc_value, in_avals)
    block_shapes = tuple(a.shape if isinstance(a, state.AbstractRef) else None
                         for a in in_avals)
    ctx = ctx.lowering_context.replace(
        block_shapes=(*ctx.block_shapes, *block_shapes)
    )
    jaxpr_subcomp(ctx, jaxpr, *consts, *args)
    tpu.YieldOp([])
  return []

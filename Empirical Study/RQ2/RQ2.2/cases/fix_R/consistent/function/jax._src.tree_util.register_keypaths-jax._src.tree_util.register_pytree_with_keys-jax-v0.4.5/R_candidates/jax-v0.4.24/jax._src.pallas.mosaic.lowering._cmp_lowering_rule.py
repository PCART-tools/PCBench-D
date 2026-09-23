def _cmp_lowering_rule(prim, ctx: LoweringRuleContext, x, y):
  x, y = _bcast(x, y, ctx.avals_in[0], ctx.avals_in[1], ctx.avals_out[0])
  x_aval, y_aval = ctx.avals_in
  dtypes = x_aval.dtype, y_aval.dtype
  if all(jnp.issubdtype(dtype, jnp.integer) for dtype in dtypes):
    pred = _cmpi_lowering_types[prim]
    predicate = ir.IntegerAttr.get(ir.IntegerType.get_signless(64), pred)
    return arith.CmpIOp(predicate, x, y).result
  elif all(jnp.issubdtype(dtype, jnp.floating) for dtype in dtypes):
    pred = _cmpf_lowering_types[prim]
    predicate = ir.IntegerAttr.get(ir.IntegerType.get_signless(64), pred)
    return arith.CmpFOp(predicate, x, y).result
  raise NotImplementedError("Mixed dtype operands in cmp")

def _reduce_max_lowering_rule(ctx: LoweringRuleContext, x, *, axes):
  (x_aval,) = ctx.avals_in
  out_type = aval_to_ir_type(ctx.avals_out[0])
  if jnp.issubdtype(x_aval.dtype, jnp.floating):
    kind = ir.Attribute.parse("#vector.kind<maxf>")
    val = ir.FloatAttr.get(ir.F32Type.get(), float("-inf"))
    identity = ir.DenseElementsAttr.get_splat(out_type, val)
  elif jnp.issubdtype(x_aval.dtype, jnp.signedinteger):
    kind = ir.Attribute.parse("#vector.kind<maxsi>")
    raise NotImplementedError
  elif jnp.issubdtype(x_aval.dtype, jnp.unsignedinteger):
    kind = ir.Attribute.parse("#vector.kind<maxui>")
    raise NotImplementedError
  acc = arith.ConstantOp(out_type, identity)
  op = vector.MultiDimReductionOp(
      kind,
      x,
      acc,
      ir.ArrayAttr.get(
          [ir.IntegerAttr.get(ir.IntegerType.get_signless(64), a) for a in axes]
      ),
  )
  return op.result

def _convert_element_type_lowering_rule(
    ctx: LoweringRuleContext, x, *, new_dtype, weak_type
):
  del weak_type
  out_aval = ctx.avals_out[0]
  old_dtype = ctx.avals_in[0].dtype
  out_type = aval_to_ir_type(out_aval)
  if old_dtype == new_dtype:
    return x
  if jnp.issubdtype(old_dtype, jnp.floating) and jnp.issubdtype(
      new_dtype, jnp.floating
  ):
    if old_dtype.itemsize < new_dtype.itemsize:
      return arith.ExtFOp(out_type, x).result
    else:
      return arith.TruncFOp(out_type, x).result
  elif old_dtype == jnp.bool_ and jnp.issubdtype(new_dtype, jnp.integer):
    return arith.ExtSIOp(out_type, x).result
  elif jnp.issubdtype(old_dtype, jnp.signedinteger) and jnp.issubdtype(
      new_dtype, jnp.floating
  ):
    return arith.SIToFPOp(out_type, x).result
  elif jnp.issubdtype(old_dtype, jnp.signedinteger) and jnp.issubdtype(
      new_dtype, jnp.signedinteger
  ):
    if old_dtype.itemsize < new_dtype.itemsize:
      return arith.ExtSIOp(out_type, x).result
    else:
      return arith.TruncIOp(out_type, x).result
  elif jnp.issubdtype(old_dtype, jnp.floating) and jnp.issubdtype(
      new_dtype, jnp.signedinteger
  ):
    return arith.FPToSIOp(out_type, x).result
  raise NotImplementedError(f"Unsupported cast: {old_dtype} -> {new_dtype}")

def _convert_element_type_lowering_rule(
    ctx: TritonLoweringRuleContext, a, *, new_dtype, weak_type
):
  if new_dtype == ctx.avals_in[0].dtype:
    return a
  if new_dtype == jnp.float32:
    new_dtype = tl.float32
  elif new_dtype == jnp.float64:
    new_dtype = tl.float64
  elif new_dtype == jnp.float16:
    new_dtype = tl.float16
  elif new_dtype == jnp.bfloat16:
    new_dtype = tl.bfloat16
  elif new_dtype == jnp.int32:
    new_dtype = tl.int32
  elif new_dtype == jnp.int64:
    new_dtype = tl.int64
  else:
    raise ValueError(f"Unhandled dtype: {new_dtype}")
  return tl.semantic.cast(a, new_dtype, ctx.builder)

def _dot_general_lowering(
    ctx: TritonLoweringRuleContext,
    a,
    b,
    *,
    dimension_numbers,
    precision,
    preferred_element_type
):
  contract_dims, batch_dims = dimension_numbers
  assert batch_dims == ((), ())
  (a_contract_dim,) = contract_dims[0]
  (b_contract_dim,) = contract_dims[1]
  trans_a = a_contract_dim == 0
  trans_b = b_contract_dim == 1
  if trans_a:
    a = tl.trans(a, _builder=ctx.builder)
  if trans_b:
    b = tl.trans(b, _builder=ctx.builder)
  allow_tf32 = (
      precision == lax.Precision.HIGH or precision == lax.Precision.DEFAULT
  )
  return tl.dot(a, b, _builder=ctx.builder, allow_tf32=allow_tf32)

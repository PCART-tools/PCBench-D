def _dot_general_lowering(
    ctx: TritonLoweringRuleContext,
    a,
    b,
    *,
    dimension_numbers,
    precision,
    preferred_element_type
):
  del preferred_element_type  # Unused.
  ((a_contract_dim,), (b_contract_dim,)), batch_dims = dimension_numbers
  assert batch_dims == ((), ())

  if a_contract_dim == 0:
    a = tc.semantic.trans(a)
  if b_contract_dim == 1:
    b = tc.semantic.trans(b)

  if precision is None:
    allow_tf32 = True
  else:
    prec_a, prec_b = precision
    allow_tf32 = prec_a in _TF32_PRECISIONS or prec_b in _TF32_PRECISIONS

  out_dtype = acc_dtype = _convert_dtype(ctx.avals_out[0].dtype)
  if acc_dtype not in (tc.int32, tc.float16):
    acc_dtype = tc.float32

  return tc.semantic.cast(
      tc.dot(
          a,
          b,
          allow_tf32=allow_tf32,
          out_dtype=acc_dtype,
      ),
      out_dtype,
  )

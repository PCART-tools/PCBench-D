def bilinear_transpose(lhs_rule, rhs_rule, cotangent, x, y, **kwargs):
  assert is_undefined_primal(x) ^ is_undefined_primal(y)
  if type(cotangent) is Zero:
    return Zero
  if is_undefined_primal(x):
    out = lhs_rule(cotangent, x, y, **kwargs)
    return Zero if out is Zero else (out, None)
  else:
    out = rhs_rule(cotangent, x, y, **kwargs)
    return Zero if out is Zero else (None, out)

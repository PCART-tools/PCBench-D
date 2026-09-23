def _tangent_linear_map(func, params, params_dot, *x):
  """Compute the tangent of a linear map.

  Assuming ``func(*params, *x)`` is linear in ``x`` and computes ``A @ x``,
  this function computes ``∂A @ x``.
  """
  assert any(type(p) is not ad_util.Zero for p in params_dot)
  zeros = _map(ad_util.Zero.from_value, x)
  _, out_tangent = ad.jvp(lu.wrap_init(func)).call_wrapped(
      params + list(x), params_dot + zeros)
  return out_tangent

def igammac_impl(a, x, *, dtype):
  out_of_range = bitwise_or(le(x, _const(x, 0)), le(a, _const(a, 0)))
  use_igamma = bitwise_or(lt(x, _const(x, 1)), lt(x, a))
  ax = a * log(x) - x - lgamma(a)
  underflow = lt(ax, -log(dtypes.finfo(dtype).max))
  enabled = bitwise_not(bitwise_or(out_of_range, underflow))
  ax = exp(ax)

  igamma_call = _igamma_series(ax, x, a, bitwise_and(enabled, use_igamma),
                               dtype, IgammaMode.VALUE)
  igammac_cf_call = _igammac_continued_fraction(ax, x, a,
    bitwise_and(enabled, bitwise_not(use_igamma)), dtype, IgammaMode.VALUE)

  result = select(use_igamma, _const(a, 1) - igamma_call, igammac_cf_call)
  x_is_infinity = eq(x, _const(x, float('inf')))
  result = select(x_is_infinity, full_like(result, 0), result)
  return select(out_of_range, full_like(a, 1), result)

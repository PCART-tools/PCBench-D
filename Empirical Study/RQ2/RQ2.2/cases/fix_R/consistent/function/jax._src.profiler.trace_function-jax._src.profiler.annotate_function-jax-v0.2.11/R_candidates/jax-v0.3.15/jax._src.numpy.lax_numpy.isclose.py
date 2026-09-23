@_wraps(np.isclose)
@partial(jit, static_argnames=('equal_nan',))
def isclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False):
  a, b = _promote_args("isclose", a, b)
  dtype = _dtype(a)
  if issubdtype(dtype, inexact):
    if issubdtype(dtype, complexfloating):
      dtype = _complex_elem_type(dtype)
    rtol = lax.convert_element_type(rtol, dtype)
    atol = lax.convert_element_type(atol, dtype)
    out = lax.le(
      lax.abs(lax.sub(a, b)),
      lax.add(atol, lax.mul(rtol, lax.abs(b))))
    # This corrects the comparisons for infinite and nan values
    a_inf = isinf(a)
    b_inf = isinf(b)
    any_inf = logical_or(a_inf, b_inf)
    both_inf = logical_and(a_inf, b_inf)
    # Make all elements where either a or b are infinite to False
    out = logical_and(out, logical_not(any_inf))
    # Make all elements where both a or b are the same inf to True
    same_value = lax.eq(a, b)
    same_inf = logical_and(both_inf, same_value)
    out = logical_or(out, same_inf)

    # Make all elements where either a or b is NaN to False
    a_nan = isnan(a)
    b_nan = isnan(b)
    any_nan = logical_or(a_nan, b_nan)
    out = logical_and(out, logical_not(any_nan))
    if equal_nan:
      # Make all elements where both a and b is NaN to True
      both_nan = logical_and(a_nan, b_nan)
      out = logical_or(out, both_nan)
    return out
  else:
    return lax.eq(a, b)

@_wraps(np.lcm, module='numpy')
@jit
def lcm(x1, x2):
  _check_arraylike("lcm", x1, x2)
  x1, x2 = _promote_dtypes(x1, x2)
  d = gcd(x1, x2)
  return where(d == 0, _lax_const(d, 0),
               abs(multiply(x1, floor_divide(x2, d))))

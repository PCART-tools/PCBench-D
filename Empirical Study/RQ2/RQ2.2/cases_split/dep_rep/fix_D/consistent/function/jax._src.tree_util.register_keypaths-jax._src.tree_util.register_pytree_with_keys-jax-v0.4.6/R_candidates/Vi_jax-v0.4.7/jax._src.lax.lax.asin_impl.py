def asin_impl(x):
  if dtypes.issubdtype(_dtype(x), np.complexfloating):
    return mul(_const(x, -1j), asinh(mul(_const(x, 1j), x)))
  else:
    return mul(_const(x, 2),
               atan2(x, add(_const(x, 1), sqrt(sub(_const(x, 1), square(x))))))

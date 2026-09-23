def acos_impl(x):
  if dtypes.issubdtype(_dtype(x), np.complexfloating):
    result = mul(_const(x, 1j), acosh(x))
    # By convention, numpy chooses the branch with positive real part.
    rpart = real(result)
    return select(
      gt(rpart, _const(rpart, 0)),
      result,
      neg(result)
    )
  else:
    return select(
        ne(x, _const(x, -1.0)),
        mul(_const(x, 2),
            atan2(sqrt(sub(_const(x, 1), square(x))), add(_const(x, 1), x))),
        full_like(x, np.pi))

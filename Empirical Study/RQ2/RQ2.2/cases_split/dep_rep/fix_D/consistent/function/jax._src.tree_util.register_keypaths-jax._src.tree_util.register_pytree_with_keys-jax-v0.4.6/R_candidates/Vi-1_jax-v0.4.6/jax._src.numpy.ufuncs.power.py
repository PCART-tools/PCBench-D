@_wraps(np.power, module='numpy')
def power(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  _check_arraylike("power", x1, x2)
  # Special case for concrete integer scalars: use binary exponentiation.
  # Using lax.pow may be imprecise for floating-point values; the goal of this
  # code path is to make sure we end up with a precise output for the common
  # pattern ``x ** 2`` or similar.
  if isinstance(core.get_aval(x2), core.ConcreteArray):
    try:
      x2 = operator.index(x2)  # type: ignore[arg-type]
    except TypeError:
      pass
    else:
      x1, = _promote_dtypes_numeric(x1)
      return lax.integer_pow(x1, x2)
  return _power(x1, x2)

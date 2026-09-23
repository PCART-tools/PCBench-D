@implements(np.power, module='numpy')
def power(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  check_arraylike("power", x1, x2)
  check_no_float0s("power", x1, x2)

  # We apply special cases, both for algorithmic and autodiff reasons:
  #  1. for *concrete* integer scalar powers (and arbitrary bases), we use
  #     unrolled binary exponentiation specialized on the exponent, which is
  #     more precise for e.g. x ** 2 when x is a float (algorithmic reason!);
  #  2. for integer bases and integer powers, use unrolled binary exponentiation
  #     where the number of steps is determined by a max bit width of 64
  #     (algorithmic reason!);
  #  3. for integer powers and float/complex bases, we apply the lax primitive
  #     without any promotion of input types because in this case we want the
  #     function to be differentiable wrt its first argument at 0;
  #  3. for other cases, perform jnp dtype promotion on the arguments then apply
  #     lax.pow.

  # Case 1: concrete integer scalar powers:
  if isinstance(core.get_aval(x2), core.ConcreteArray):
    try:
      x2 = operator.index(x2)  # type: ignore[arg-type]
    except TypeError:
      pass
    else:
      x1, = promote_dtypes_numeric(x1)
      return lax.integer_pow(x1, x2)

  # Handle cases #2 and #3 under a jit:
  return _power(x1, x2)

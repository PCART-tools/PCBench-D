@jit
def lcm(x1: ArrayLike, x2: ArrayLike) -> Array:
  """Compute the least common multiple of two arrays.

  JAX implementation of :func:`numpy.lcm`.

  Args:
    x1: First input array. The elements must have integer dtype.
    x2: Second input array. The elements must have integer dtype.

  Returns:
    An array containing the least common multiple of the corresponding
    elements from the absolute values of `x1` and `x2`.

  See also:
    - :func:`jax.numpy.gcd`: compute the greatest common divisor of two arrays.

  Examples:
    Scalar inputs:

    >>> jnp.lcm(12, 18)
    Array(36, dtype=int32, weak_type=True)

    Array inputs:

    >>> x1 = jnp.array([12, 18, 24])
    >>> x2 = jnp.array([5, 10, 15])
    >>> jnp.lcm(x1, x2)
    Array([ 60,  90, 120], dtype=int32)

    Broadcasting:

    >>> x1 = jnp.array([12])
    >>> x2 = jnp.array([6, 9, 12])
    >>> jnp.lcm(x1, x2)
    Array([12, 36, 12], dtype=int32)
  """
  util.check_arraylike("lcm", x1, x2)
  x1, x2 = util.promote_dtypes(x1, x2)
  x1, x2 = ufuncs.abs(x1), ufuncs.abs(x2)
  if not issubdtype(_dtype(x1), integer):
    raise ValueError("Arguments to jax.numpy.lcm must be integers.")
  d = gcd(x1, x2)
  return where(d == 0, _lax_const(d, 0),
               ufuncs.multiply(x1, ufuncs.floor_divide(x2, d)))

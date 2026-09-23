@jit
def gcd(x1: ArrayLike, x2: ArrayLike) -> Array:
  """Compute the greatest common divisor of two arrays.

  JAX implementation of :func:`numpy.gcd`.

  Args:
    x1: First input array. The elements must have integer dtype.
    x2: Second input array. The elements must have integer dtype.

  Returns:
    An array containing the greatest common divisors of the corresponding
    elements from the absolute values of `x1` and `x2`.

  See also:
    - :func:`jax.numpy.lcm`: compute the least common multiple of two arrays.

  Examples:
    Scalar inputs:

    >>> jnp.gcd(12, 18)
    Array(6, dtype=int32, weak_type=True)

    Array inputs:

    >>> x1 = jnp.array([12, 18, 24])
    >>> x2 = jnp.array([5, 10, 15])
    >>> jnp.gcd(x1, x2)
    Array([1, 2, 3], dtype=int32)

    Broadcasting:

    >>> x1 = jnp.array([12])
    >>> x2 = jnp.array([6, 9, 12])
    >>> jnp.gcd(x1, x2)
    Array([ 6,  3, 12], dtype=int32)
  """
  util.check_arraylike("gcd", x1, x2)
  x1, x2 = util.promote_dtypes(x1, x2)
  if not issubdtype(_dtype(x1), integer):
    raise ValueError("Arguments to jax.numpy.gcd must be integers.")
  x1, x2 = broadcast_arrays(x1, x2)
  gcd, _ = lax.while_loop(_gcd_cond_fn, _gcd_body_fn, (ufuncs.abs(x1), ufuncs.abs(x2)))
  return gcd

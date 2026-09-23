def array_equal(a1: ArrayLike, a2: ArrayLike, equal_nan: bool = False) -> Array:
  """Check if two arrays are element-wise equal.

  JAX implementation of :func:`numpy.array_equal`.

  Args:
    a1: first input array to compare.
    a2: second input array to compare.
    equal_nan: Boolean. If ``True``, NaNs in ``a1`` will be considered
      equal to NaNs in ``a2``. Default is ``False``.

  Returns:
    Boolean scalar array indicating whether the input arrays are element-wise equal.

  See Also:
    - :func:`jax.numpy.allclose`
    - :func:`jax.numpy.array_equiv`

  Examples:
    >>> jnp.array_equal(jnp.array([1, 2, 3]), jnp.array([1, 2, 3]))
    Array(True, dtype=bool)
    >>> jnp.array_equal(jnp.array([1, 2, 3]), jnp.array([1, 2]))
    Array(False, dtype=bool)
    >>> jnp.array_equal(jnp.array([1, 2, 3]), jnp.array([1, 2, 4]))
    Array(False, dtype=bool)
    >>> jnp.array_equal(jnp.array([1, 2, float('nan')]),
    ...                 jnp.array([1, 2, float('nan')]))
    Array(False, dtype=bool)
    >>> jnp.array_equal(jnp.array([1, 2, float('nan')]),
    ...                 jnp.array([1, 2, float('nan')]), equal_nan=True)
    Array(True, dtype=bool)
  """
  a1, a2 = asarray(a1), asarray(a2)
  if shape(a1) != shape(a2):
    return bool_(False)
  eq = asarray(a1 == a2)
  if equal_nan:
    eq = ufuncs.logical_or(eq, ufuncs.logical_and(ufuncs.isnan(a1), ufuncs.isnan(a2)))
  return reductions.all(eq)

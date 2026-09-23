def array_equiv(a1: ArrayLike, a2: ArrayLike) -> Array:
  """Check if two arrays are element-wise equal.

  JAX implementation of :func:`numpy.array_equiv`.

  This function will return ``False`` if the input arrays cannot be broadcasted
  to the same shape.

  Args:
    a1: first input array to compare.
    a2: second input array to compare.

  Returns:
    Boolean scalar array indicating whether the input arrays are
    element-wise equal after broadcasting.

  See Also:
    - :func:`jax.numpy.allclose`
    - :func:`jax.numpy.array_equal`

  Examples:
    >>> jnp.array_equiv(jnp.array([1, 2, 3]), jnp.array([1, 2, 3]))
    Array(True, dtype=bool)
    >>> jnp.array_equiv(jnp.array([1, 2, 3]), jnp.array([1, 2, 4]))
    Array(False, dtype=bool)
    >>> jnp.array_equiv(jnp.array([[1, 2, 3], [1, 2, 3]]),
    ...                 jnp.array([1, 2, 3]))
    Array(True, dtype=bool)
  """
  a1, a2 = asarray(a1), asarray(a2)
  try:
    eq = ufuncs.equal(a1, a2)
  except ValueError:
    # shapes are not broadcastable
    return bool_(False)
  return reductions.all(eq)

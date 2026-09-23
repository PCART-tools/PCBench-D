@jit
def iscomplex(x: ArrayLike) -> Array:
  """Return boolean array showing where the input is complex.

  JAX implementation of :func:`numpy.iscomplex`.

  Args:
    x: Input array to check.

  Returns:
    A new array containing boolean values indicating complex elements.

  See Also:
    - :func:`jax.numpy.iscomplexobj`
    - :func:`jax.numpy.isrealobj`

  Examples:
    >>> jnp.iscomplex(jnp.array([True, 0, 1, 2j, 1+2j]))
    Array([False, False, False, True, True], dtype=bool)
  """
  i = ufuncs.imag(x)
  return lax.ne(i, _lax_const(i, 0))

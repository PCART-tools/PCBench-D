@jit
def isreal(x: ArrayLike) -> Array:
  """Return boolean array showing where the input is real.

  JAX implementation of :func:`numpy.isreal`.

  Args:
    x: input array to check.

  Returns:
    A new array containing boolean values indicating real elements.

  See Also:
    - :func:`jax.numpy.iscomplex`
    - :func:`jax.numpy.isrealobj`

  Examples:
    >>> jnp.isreal(jnp.array([False, 0j, 1, 2.1, 1+2j]))
    Array([ True,  True,  True,  True, False], dtype=bool)
  """
  i = ufuncs.imag(x)
  return lax.eq(i, _lax_const(i, 0))

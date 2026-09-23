@jit
def logaddexp(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Compute ``log(exp(x1) + exp(x2))`` avoiding overflow.

  JAX implementation of :obj:`numpy.logaddexp`

  Args:
    x1: input array
    x2: input array

  Returns:
    array containing the result.

  Examples:

  >>> x1 = jnp.array([1, 2, 3])
  >>> x2 = jnp.array([4, 5, 6])
  >>> result1 = jnp.logaddexp(x1, x2)
  >>> result2 = jnp.log(jnp.exp(x1) + jnp.exp(x2))
  >>> print(jnp.allclose(result1, result2))
  True
  """
  x1, x2 = promote_args_inexact("logaddexp", x1, x2)
  return lax_other.logaddexp(x1, x2)

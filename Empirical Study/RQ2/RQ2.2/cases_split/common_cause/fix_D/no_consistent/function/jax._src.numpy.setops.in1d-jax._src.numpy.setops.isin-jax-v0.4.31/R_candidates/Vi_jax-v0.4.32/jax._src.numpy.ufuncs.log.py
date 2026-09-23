@partial(jit, inline=True)
def log(x: ArrayLike, /) -> Array:
  """Calculate element-wise natural logarithm of the input.

  JAX implementation of :obj:`numpy.log`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing the logarithm of each element in ``x``, promotes to inexact
    dtype.

  See also:
    - :func:`jax.numpy.exp`: Calculates element-wise exponential of the input.
    - :func:`jax.numpy.log2`: Calculates base-2 logarithm of each element of input.
    - :func:`jax.numpy.log1p`: Calculates element-wise logarithm of one plus input.

  Examples:
    ``jnp.log`` and ``jnp.exp`` are inverse functions of each other. Applying
    ``jnp.log`` on the result of ``jnp.exp(x)`` yields the original input ``x``.

    >>> x = jnp.array([2, 3, 4, 5])
    >>> jnp.log(jnp.exp(x))
    Array([2., 3., 4., 5.], dtype=float32)

    Using ``jnp.log`` we can demonstrate well-known properties of logarithms, such
    as :math:`log(a*b) = log(a)+log(b)`.

    >>> x1 = jnp.array([2, 1, 3, 1])
    >>> x2 = jnp.array([1, 3, 2, 4])
    >>> jnp.allclose(jnp.log(x1*x2), jnp.log(x1)+jnp.log(x2))
    Array(True, dtype=bool)
  """
  return lax.log(*promote_args_inexact('log', x))

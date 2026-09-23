@partial(jit, inline=True)
def log1p(x: ArrayLike, /) -> Array:
  """Calculates element-wise logarithm of one plus input, ``log(x+1)``.

  JAX implementation of :obj:`numpy.log1p`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing the logarithm of one plus of each element in ``x``,
    promotes to inexact dtype.

  Note:
    ``jnp.log1p`` is more accurate than when using the naive computation of
    ``log(x+1)`` for small values of ``x``.

  See also:
    - :func:`jax.numpy.expm1`: Calculates :math:`e^x-1` of each element of the
      input.
    - :func:`jax.numpy.log2`: Calculates base-2 logarithm of each element of input.
    - :func:`jax.numpy.log`: Calculates element-wise logarithm of the input.

  Examples:
    >>> x = jnp.array([2, 5, 9, 4])
    >>> jnp.allclose(jnp.log1p(x), jnp.log(x+1))
    Array(True, dtype=bool)

    For values very close to 0, ``jnp.log1p(x)`` is more accurate than
    ``jnp.log(x+1)``:

    >>> x1 = jnp.array([1e-4, 1e-6, 2e-10])
    >>> jnp.expm1(jnp.log1p(x1))  # doctest: +SKIP
    Array([1.00000005e-04, 9.99999997e-07, 2.00000003e-10], dtype=float32)
    >>> jnp.expm1(jnp.log(x1+1))  # doctest: +SKIP
    Array([1.000166e-04, 9.536743e-07, 0.000000e+00], dtype=float32)
  """
  return lax.log1p(*promote_args_inexact('log1p', x))

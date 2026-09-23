@partial(jit, inline=True)
def ceil(x: ArrayLike, /) -> Array:
  """Round input to the nearest integer upwards.

  JAX implementation of :obj:`numpy.ceil`.

  Args:
    x: input array or scalar. Must not have complex dtype.

  Returns:
    An array with same shape and dtype as ``x`` containing the values rounded to
    the nearest integer that is greater than or equal to the value itself.

  See also:
    - :func:`jax.numpy.fix`: Rounds the input to the nearest interger towards zero.
    - :func:`jax.numpy.trunc`: Rounds the input to the nearest interger towards
      zero.
    - :func:`jax.numpy.floor`: Rounds the input down to the nearest integer.

  Examples:
    >>> key = jax.random.key(1)
    >>> x = jax.random.uniform(key, (3, 3), minval=-5, maxval=5)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(x)
    [[ 2.55 -1.87 -3.76]
     [ 0.48  3.85 -1.94]
     [ 3.2   4.56 -1.43]]
    >>> jnp.ceil(x)
    Array([[ 3., -1., -3.],
           [ 1.,  4., -1.],
           [ 4.,  5., -1.]], dtype=float32)
  """
  check_arraylike('ceil', x)
  if dtypes.isdtype(dtypes.dtype(x), ('integral', 'bool')):
    return lax.asarray(x)
  return lax.ceil(*promote_args_inexact('ceil', x))

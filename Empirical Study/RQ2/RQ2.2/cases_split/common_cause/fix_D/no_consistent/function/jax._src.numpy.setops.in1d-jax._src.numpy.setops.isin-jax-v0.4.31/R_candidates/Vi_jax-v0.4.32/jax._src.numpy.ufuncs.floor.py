@partial(jit, inline=True)
def floor(x: ArrayLike, /) -> Array:
  """Round input to the nearest integer downwards.

  JAX implementation of :obj:`numpy.floor`.

  Args:
    x: input array or scalar. Must not have complex dtype.

  Returns:
    An array with same shape and dtype as ``x`` containing the values rounded to
    the nearest integer that is less than or equal to the value itself.

  See also:
    - :func:`jax.numpy.fix`: Rounds the input to the nearest interger towards zero.
    - :func:`jax.numpy.trunc`: Rounds the input to the nearest interger towards
      zero.
    - :func:`jax.numpy.ceil`: Rounds the input up to the nearest integer.

  Examples:
    >>> key = jax.random.key(42)
    >>> x = jax.random.uniform(key, (3, 3), minval=-5, maxval=5)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(x)
    [[ 1.44 -1.77 -3.07]
     [ 3.86  2.25 -3.08]
     [-1.55 -2.48  1.32]]
    >>> jnp.floor(x)
    Array([[ 1., -2., -4.],
           [ 3.,  2., -4.],
           [-2., -3.,  1.]], dtype=float32)
  """
  check_arraylike('floor', x)
  if dtypes.isdtype(dtypes.dtype(x), ('integral', 'bool')):
    return lax.asarray(x)
  return lax.floor(*promote_args_inexact('floor', x))

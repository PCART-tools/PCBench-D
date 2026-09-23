@jit
def trunc(x: ArrayLike) -> Array:
  """Round input to the nearest integer towards zero.

  JAX implementation of :func:`numpy.trunc`.

  Args:
    x: input array or scalar.

  Returns:
    An array with same shape and dtype as ``x`` containing the rounded values.

  See also:
    - :func:`jax.numpy.fix`: Rounds the input to the nearest integer towards zero.
    - :func:`jax.numpy.ceil`: Rounds the input up to the nearest integer.
    - :func:`jax.numpy.floor`: Rounds the input down to the nearest integer.

  Examples:
    >>> key = jax.random.key(42)
    >>> x = jax.random.uniform(key, (3, 3), minval=-10, maxval=10)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(x)
    [[ 2.88 -3.55 -6.13]
     [ 7.73  4.49 -6.16]
     [-3.1  -4.95  2.64]]
    >>> jnp.trunc(x)
    Array([[ 2., -3., -6.],
           [ 7.,  4., -6.],
           [-3., -4.,  2.]], dtype=float32)
  """
  util.check_arraylike('trunc', x)
  if dtypes.isdtype(dtypes.dtype(x), ('integral', 'bool')):
    return lax_internal.asarray(x)
  return where(lax.lt(x, _lax_const(x, 0)), ufuncs.ceil(x), ufuncs.floor(x))

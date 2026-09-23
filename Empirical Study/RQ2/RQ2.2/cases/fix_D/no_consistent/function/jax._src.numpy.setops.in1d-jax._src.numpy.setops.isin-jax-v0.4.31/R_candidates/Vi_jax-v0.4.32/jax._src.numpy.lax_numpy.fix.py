@jit
def fix(x: ArrayLike, out: None = None) -> Array:
  """Round input to the nearest integer towards zero.

  JAX implementation of :func:`numpy.fix`.

  Args:
    x: input array.
    out: unused by JAX.

  Returns:
    An array with same shape and dtype as ``x`` containing the rounded values.

  See also:
    - :func:`jax.numpy.trunc`: Rounds the input to nearest integer towards zero.
    - :func:`jax.numpy.ceil`: Rounds the input up to the nearest integer.
    - :func:`jax.numpy.floor`: Rounds the input down to the nearest integer.

  Examples:
    >>> key = jax.random.key(0)
    >>> x = jax.random.uniform(key, (3, 3), minval=-5, maxval=5)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(x)
    [[-1.45  1.04 -0.72]
     [-2.69  1.74 -0.6 ]
     [-2.49 -2.23  2.68]]
    >>> jnp.fix(x)
    Array([[-1.,  1., -0.],
           [-2.,  1., -0.],
           [-2., -2.,  2.]], dtype=float32)
  """
  util.check_arraylike("fix", x)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.fix is not supported.")
  zero = _lax_const(x, 0)
  return where(lax.ge(x, zero), ufuncs.floor(x), ufuncs.ceil(x))

def uniform(scale=1e-2, dtype: DType = jnp.float_) -> Callable:
  """Builds an initializer that returns real uniformly-distributed random arrays.

  Args:
    scale: optional; the upper bound of the random distribution.
    dtype: optional; the initializer's default dtype.

  Returns:
    An initializer that returns arrays whose values are uniformly distributed in
    the range ``[0, scale)``.

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.uniform(10.0)
  >>> initializer(jax.random.PRNGKey(42), (2, 3), jnp.float32)  # doctest: +SKIP
  DeviceArray([[7.298188 , 8.691938 , 8.7230015],
               [2.0818567, 1.8662417, 5.5022564]], dtype=float32)
  """
  def init(key, shape, dtype=dtype):
    dtype = dtypes.canonicalize_dtype(dtype)
    return random.uniform(key, shape, dtype) * scale
  return init

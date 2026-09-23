def ones(key, shape, dtype: DType = jnp.float_):
  """An initializer that returns a constant array full of ones.

  The ``key`` argument is ignored.

  >>> import jax, jax.numpy as jnp
  >>> jax.nn.initializers.ones(jax.random.PRNGKey(42), (3, 2), jnp.float32)
  DeviceArray([[1., 1.],
               [1., 1.],
               [1., 1.]], dtype=float32)
  """
  return jnp.ones(shape, dtypes.canonicalize_dtype(dtype))

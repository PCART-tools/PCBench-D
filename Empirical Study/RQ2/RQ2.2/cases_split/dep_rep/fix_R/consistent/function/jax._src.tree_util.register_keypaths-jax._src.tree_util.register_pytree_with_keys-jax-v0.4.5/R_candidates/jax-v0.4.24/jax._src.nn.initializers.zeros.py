@export
def zeros(key: KeyArray,
          shape: core.Shape,
          dtype: DTypeLikeInexact = jnp.float_) -> Array:
  """An initializer that returns a constant array full of zeros.

  The ``key`` argument is ignored.

  >>> import jax, jax.numpy as jnp
  >>> jax.nn.initializers.zeros(jax.random.PRNGKey(42), (2, 3), jnp.float32)
  Array([[0., 0., 0.],
         [0., 0., 0.]], dtype=float32)
  """
  return jnp.zeros(shape, dtypes.canonicalize_dtype(dtype))

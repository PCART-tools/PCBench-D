def normal(stddev: RealNumeric = 1e-2,
           dtype: DTypeLikeInexact = jnp.float_) -> Initializer:
  """Builds an initializer that returns real normally-distributed random arrays.

  Args:
    stddev: optional; the standard deviation of the distribution.
    dtype: optional; the initializer's default dtype.

  Returns:
    An initializer that returns arrays whose values are normally distributed
    with mean ``0`` and standard deviation ``stddev``.

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.normal(5.0)
  >>> initializer(jax.random.PRNGKey(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 3.0613258 ,  5.6129413 ,  5.6866574 ],
         [-4.063663  , -4.4520254 ,  0.63115686]], dtype=float32)
   """
  def init(key: KeyArray,
           shape: core.Shape,
           dtype: DTypeLikeInexact = dtype) -> Array:
    dtype = dtypes.canonicalize_dtype(dtype)
    return random.normal(key, shape, dtype) * stddev
  return init

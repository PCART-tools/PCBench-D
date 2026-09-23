@export
def truncated_normal(stddev: RealNumeric = 1e-2,
                     dtype: DTypeLikeInexact = jnp.float_,
                     lower: RealNumeric = -2.0,
                     upper: RealNumeric = 2.0) -> Initializer:
  r"""Builds an initializer that returns truncated-normal random arrays.

  Args:
    stddev: optional; the standard deviation of the untruncated distribution.
      Note that this function does not apply the stddev correction as is done in
      the variancescaling initializers, and users are expected to apply this
      correction themselves via the stddev arg if they wish to employ it.
    dtype: optional; the initializer's default dtype.
    lower: Float representing the lower bound for truncation. Applied before
      the output is multiplied by the stddev.
    upper: Float representing the upper bound for truncation. Applied before
      the output is multiplied by the stddev.

  Returns:
    An initializer that returns arrays whose values follow the truncated normal
    distribution with mean ``0`` and standard deviation ``stddev``, and range
    :math:`\rm{lower * stddev} < x < \rm{upper * stddev}`.

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.truncated_normal(5.0)
  >>> initializer(jax.random.PRNGKey(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 2.9047365,  5.2338114,  5.29852  ],
         [-3.836303 , -4.192359 ,  0.6022964]], dtype=float32)
  """

  def init(key: KeyArray,
           shape: core.Shape,
           dtype: DTypeLikeInexact = dtype) -> Array:
    dtype = dtypes.canonicalize_dtype(dtype)
    return random.truncated_normal(key, lower, upper, shape, dtype) * stddev
  return init

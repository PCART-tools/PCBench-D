@export
class extended(np.generic):
  """Scalar class for extended dtypes.

  This is an abstract class that should never be instantiated, but rather
  exists for the sake of `jnp.issubdtype`.

  Examples:
    >>> from jax import random
    >>> from jax import dtypes
    >>> key = random.key(0)
    >>> jnp.issubdtype(key.dtype, dtypes.extended)
    True
  """

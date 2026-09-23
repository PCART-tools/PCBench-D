def _arraylike(x):
  return (isinstance(x, np.ndarray) or isinstance(x, ndarray) or
          hasattr(x, '__jax_array__') or np.isscalar(x))

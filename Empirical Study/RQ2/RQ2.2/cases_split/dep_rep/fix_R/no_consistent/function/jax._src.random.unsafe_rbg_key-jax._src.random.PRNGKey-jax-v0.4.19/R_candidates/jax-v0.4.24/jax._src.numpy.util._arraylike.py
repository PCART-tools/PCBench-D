def _arraylike(x: ArrayLike) -> bool:
  return (isinstance(x, np.ndarray) or isinstance(x, Array) or
          hasattr(x, '__jax_array__') or np.isscalar(x))

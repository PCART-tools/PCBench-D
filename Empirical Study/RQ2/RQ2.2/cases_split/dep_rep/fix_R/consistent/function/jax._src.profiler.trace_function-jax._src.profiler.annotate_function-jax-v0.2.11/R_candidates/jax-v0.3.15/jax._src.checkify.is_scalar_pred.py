def is_scalar_pred(pred) -> bool:
  return (isinstance(pred, bool) or
          isinstance(pred, jnp.ndarray) and pred.shape == () and
          pred.dtype == jnp.dtype('bool'))

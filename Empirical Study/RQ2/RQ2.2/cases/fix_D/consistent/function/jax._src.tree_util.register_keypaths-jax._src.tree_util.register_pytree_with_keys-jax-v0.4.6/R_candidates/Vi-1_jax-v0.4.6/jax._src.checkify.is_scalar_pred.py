def is_scalar_pred(pred) -> bool:
  return (isinstance(pred, bool) or
          isinstance(pred, jax.Array) and pred.shape == () and
          pred.dtype == jnp.dtype('bool'))

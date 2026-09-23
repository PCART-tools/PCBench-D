@partial(jax.custom_jvp, nondiff_argnums=(1,))
def _softmax(
    x: ArrayLike,
    axis: Optional[Union[int, tuple[int, ...]]] = -1,
    where: Optional[ArrayLike] = None,
    initial: Optional[ArrayLike] = None) -> Array:
  x_max = jnp.max(x, axis, where=where, initial=initial, keepdims=True)
  unnormalized = jnp.exp(x - x_max)
  result = unnormalized / jnp.sum(unnormalized, axis, where=where, keepdims=True)
  if where is not None:
    result = jnp.where(where, result, 0)
  return result

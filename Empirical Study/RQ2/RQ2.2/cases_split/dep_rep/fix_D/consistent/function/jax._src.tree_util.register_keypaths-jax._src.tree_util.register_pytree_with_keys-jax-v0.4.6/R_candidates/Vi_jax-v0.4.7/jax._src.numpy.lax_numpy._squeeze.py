@partial(jit, static_argnames=('axis',), inline=True)
def _squeeze(a: Array, axis: Tuple[int]) -> Array:
  if axis is None:
    a_shape = shape(a)
    if not core.is_constant_shape(a_shape):
      # We do not even know the rank of the output if the input shape is not known
      raise ValueError("jnp.squeeze with axis=None is not supported with shape polymorphism")
    axis = tuple(i for i, d in enumerate(a_shape) if d == 1)
  return lax.squeeze(a, axis)

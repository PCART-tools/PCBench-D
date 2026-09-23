@partial(jax.jit, static_argnames=("axis",))
def glu(x: Array, axis: int = -1) -> Array:
  """Gated linear unit activation function.

  Args:
    x : input array
    axis: the axis along which the split should be computed (default: -1)
  """
  size = x.shape[axis]
  assert size % 2 == 0, "axis size must be divisible by 2"
  x1, x2 = jnp.split(x, 2, axis)
  return x1 * sigmoid(x2)

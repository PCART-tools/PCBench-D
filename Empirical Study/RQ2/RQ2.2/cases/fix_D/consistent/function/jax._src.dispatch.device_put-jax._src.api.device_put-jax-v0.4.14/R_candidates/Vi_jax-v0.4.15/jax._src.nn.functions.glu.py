@partial(jax.jit, static_argnames=("axis",))
def glu(x: Array, axis: int = -1) -> Array:
  r"""Gated linear unit activation function.

  Computes the function:

  .. math::
    \mathrm{glu}(x) =  x\left[\ldots, 0:\frac{n}{2}, \ldots\right] \cdot
      \mathrm{sigmoid} \left( x\left[\ldots, \frac{n}{2}:n, \ldots\right]
        \right)

  where the array is split into two along ``axis``. The size of the ``axis``
  dimension must be divisible by two.

  Args:
    x : input array
    axis: the axis along which the split should be computed (default: -1)

  Returns:
    An array.

  See also:
    :func:`sigmoid`
  """
  size = x.shape[axis]
  assert size % 2 == 0, "axis size must be divisible by 2"
  x1, x2 = jnp.split(x, 2, axis)
  return x1 * sigmoid(x2)

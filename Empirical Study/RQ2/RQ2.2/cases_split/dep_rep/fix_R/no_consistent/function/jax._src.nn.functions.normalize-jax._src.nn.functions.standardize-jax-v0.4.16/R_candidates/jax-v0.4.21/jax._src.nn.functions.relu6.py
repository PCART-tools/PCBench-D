@jax.custom_jvp
@jax.jit
def relu6(x: ArrayLike) -> Array:
  r"""Rectified Linear Unit 6 activation function.

  Computes the element-wise function

  .. math::
    \mathrm{relu6}(x) = \min(\max(x, 0), 6)

  except under differentiation, we take:

  .. math::
    \nabla \mathrm{relu}(0) = 0

  and

  .. math::
    \nabla \mathrm{relu}(6) = 0

  Args:
    x : input array

  Returns:
    An array.

  See also:
    :func:`relu`
  """
  return jnp.minimum(jnp.maximum(x, 0), 6.)

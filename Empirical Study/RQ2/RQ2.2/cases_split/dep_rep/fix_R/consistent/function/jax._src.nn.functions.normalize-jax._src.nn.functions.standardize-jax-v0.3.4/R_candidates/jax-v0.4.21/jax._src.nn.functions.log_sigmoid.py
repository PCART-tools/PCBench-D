@jax.jit
def log_sigmoid(x: ArrayLike) -> Array:
  r"""Log-sigmoid activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{log\_sigmoid}(x) = \log(\mathrm{sigmoid}(x)) = -\log(1 + e^{-x})

  Args:
    x : input array

  Returns:
    An array.

  See also:
    :func:`sigmoid`
  """
  numpy_util.check_arraylike("log_sigmoid", x)
  x_arr = jnp.asarray(x)
  return -softplus(-x_arr)

def create_identity_with_grad_check_fn(expected_gradient, expected_dtype=None):
  """Returns a function that asserts it's gradient has a certain value.

  This serves as a hook to assert intermediate gradients have a certain value.
  This returns an identity function. The identity's gradient function is also
  the identity function, except it asserts that the gradient equals
  `expected_gradient` and has dtype `expected_dtype`.

  Args:
    expected_gradient: The gradient function asserts that the gradient is this
      value.
    expected_dtype: The gradient function asserts the gradient has this dtype.

  Returns:
    An identity function whose gradient function asserts the gradient has a
    certain value.
  """
  @custom_gradient.custom_gradient
  def _identity_with_grad_check(x):
    """Function that asserts it's gradient has a certain value."""
    x = array_ops.identity(x)
    def grad(dx):
      """Gradient function that asserts the gradient has a certain value."""
      if expected_dtype:
        assert dx.dtype == expected_dtype, (
            'dx.dtype should be %s but is: %s' % (expected_dtype, dx.dtype))
      expected_tensor = ops.convert_to_tensor_v2(
          expected_gradient, dtype=dx.dtype, name='expected_gradient')
      # Control dependency is to ensure input is available. It's possible the
      # dataset will throw a StopIteration to indicate there is no more data, in
      # which case we don't want to run the assertion.
      with ops.control_dependencies([x]):
        assert_op = check_ops.assert_equal(dx, expected_tensor)
      with ops.control_dependencies([assert_op]):
        dx = array_ops.identity(dx)
      return dx
    return x, grad
  # Keras sometimes has trouble serializing Lambda layers with a decorated
  # function. So we define and return a non-decorated function.
  def identity_with_grad_check(x):
    return _identity_with_grad_check(x)
  return identity_with_grad_check

def _is_all_finite(grads):
  """Returns a scalar boolean tensor indicating if all gradients are finite."""
  is_finite_per_grad = [
      math_ops.reduce_all(math_ops.is_finite(g)) for g in grads if g is not None
  ]
  return math_ops.reduce_all(is_finite_per_grad)

def _defer_to_unrecognized_arg(opchar, binary_op, swap=False):
  # Ensure that other array types have the chance to override arithmetic.
  def deferring_binary_op(self, other):
    if hasattr(other, '__jax_array__'):
      other = other.__jax_array__()
    args = (other, self) if swap else (self, other)
    if isinstance(other, _accepted_binop_types):
      return binary_op(*args)
    if isinstance(other, _rejected_binop_types):
      raise TypeError(f"unsupported operand type(s) for {opchar}: "
                      f"{type(args[0]).__name__!r} and {type(args[1]).__name__!r}")
    return NotImplemented
  return deferring_binary_op

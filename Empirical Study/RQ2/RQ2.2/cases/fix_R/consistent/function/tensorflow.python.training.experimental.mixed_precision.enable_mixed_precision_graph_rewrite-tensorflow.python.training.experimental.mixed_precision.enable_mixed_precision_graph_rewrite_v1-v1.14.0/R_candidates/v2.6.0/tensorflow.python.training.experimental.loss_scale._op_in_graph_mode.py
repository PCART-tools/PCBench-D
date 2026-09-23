def _op_in_graph_mode(tensor):
  """Returns the tensor's op in graph mode, or the tensor in eager mode.

  This is useful because sometimes an op is needed in graph mode instead of a
  tensor. In eager mode, there are no ops.

  Args:
    tensor: A tensor.

  Returns:
    The tensor's op in graph mode. The tensor in eager mode.
  """
  if context.executing_eagerly():
    return tensor
  return tensor.op

def _assign_if_finite(var, value):
  """Assigns a value to a variable if the value is finite."""
  return control_flow_ops.cond(
      math_ops.is_finite(value), lambda: _op_in_graph_mode(var.assign(value)),
      control_flow_ops.no_op)

def _broadcast_in_dim_jvp_rule(primals, tangents, *, shape, broadcast_dimensions):
  operand, *dyn_shape = primals
  operand_dot, *_ = tangents
  y = broadcast_in_dim_p.bind(operand, *dyn_shape, shape=shape,
                              broadcast_dimensions=broadcast_dimensions)
  if type(operand_dot) is ad_util.Zero:
    y_dot = ad_util.Zero.from_value(y)
  else:
    y_dot = broadcast_in_dim_p.bind(operand_dot, *dyn_shape, shape=shape,
                                    broadcast_dimensions=broadcast_dimensions)
  return y, y_dot

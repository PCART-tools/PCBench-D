def _comparator_builder(op_type, is_max_k):
  c = xc.XlaBuilder(
      'top_k_{}_comparator'.format('gt' if is_max_k else 'lt'))
  p0 = xla.parameter(c, 0, xc.Shape.scalar_shape(op_type))
  p1 = xla.parameter(c, 1, xc.Shape.scalar_shape(op_type))
  xla.parameter(c, 2, xc.Shape.scalar_shape(np.dtype(np.int32)))
  xla.parameter(c, 3, xc.Shape.scalar_shape(np.dtype(np.int32)))
  if is_max_k:
    cmp_result = xc.ops.Gt(p0, p1)
  else:
    cmp_result = xc.ops.Lt(p0, p1)
  return c.build(cmp_result)

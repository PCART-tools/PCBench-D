def _approx_top_k_fallback_translation(ctx, avals_in, avals_out, operand, *, k,
                                       reduction_dimension, recall_target,
                                       is_max_k, reduction_input_size_override,
                                       aggregate_to_topk):
  c = ctx.builder
  op_shape = c.get_shape(operand)
  if not op_shape.is_array():
    raise ValueError(f'operand must be an array, but was {op_shape}')
  op_dims = op_shape.dimensions()
  op_type = op_shape.element_type()

  if reduction_dimension < 0:
    reduction_dimension = len(op_dims) + reduction_dimension
  comparator = _comparator_builder(op_type, is_max_k)
  iota = xc.ops.Iota(c, xc.Shape.array_shape(np.dtype(np.int32), op_dims),
                     reduction_dimension)
  init_val_literal = _get_init_val_literal(op_type, is_max_k)
  init_val = xc.ops.Constant(c, init_val_literal)
  init_arg = xc.ops.Constant(c, np.int32(-1))
  out = xc.ops.ApproxTopKFallback(c, [operand, iota], [init_val, init_arg], k,
                                  reduction_dimension, comparator,
                                  recall_target, aggregate_to_topk,
                                  reduction_input_size_override)
  return xla.xla_destructure(c, out)

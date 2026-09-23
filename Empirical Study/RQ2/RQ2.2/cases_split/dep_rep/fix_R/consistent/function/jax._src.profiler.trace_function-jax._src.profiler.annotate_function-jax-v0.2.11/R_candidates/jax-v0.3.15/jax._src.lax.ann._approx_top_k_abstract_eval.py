def _approx_top_k_abstract_eval(operand, *, k, reduction_dimension,
                                recall_target, is_max_k,
                                reduction_input_size_override,
                                aggregate_to_topk):
  if k <= 0:
    raise ValueError(f'k must be positive, got {k}')
  if len(operand.shape) == 0:
    raise TypeError('approx_top_k operand must have >= 1 dimension, got {}'.format(
        operand.shape))
  dims = list(operand.shape)
  if dims[reduction_dimension] < k:
    raise ValueError(
        'k must be smaller than the size of reduction_dim {}, got {}'.format(
            dims[reduction_dimension], k))
  if not dtypes.issubdtype(operand.dtype, np.floating):
    raise ValueError('operand must be a floating type')
  reduction_input_size = dims[reduction_dimension]
  dims[reduction_dimension] = xc.ops.ApproxTopKReductionOutputSize(
      reduction_input_size, len(dims), k, recall_target, aggregate_to_topk,
      reduction_input_size_override)[0]
  return (operand.update(
      shape=dims, dtype=operand.dtype, weak_type=operand.weak_type),
          operand.update(shape=dims, dtype=np.dtype(np.int32)))

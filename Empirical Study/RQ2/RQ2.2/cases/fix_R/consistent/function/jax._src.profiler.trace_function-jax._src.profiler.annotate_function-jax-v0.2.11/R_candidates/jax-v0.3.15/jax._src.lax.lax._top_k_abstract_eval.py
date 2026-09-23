def _top_k_abstract_eval(operand, *, k):
  if k < 0:
    raise ValueError(f"k argument to top_k must be nonnegative, got {k}")
  if len(operand.shape) == 0:
    raise TypeError("top_k operand must have >= 1 dimension, got {}"
                    .format(operand.shape))
  shape = list(operand.shape)
  if shape[-1] < k:
    msg = "k argument to top_k must be no larger than minor dimension; {} vs {}"
    raise ValueError(msg.format(k, shape))
  shape[-1] = k
  return (operand.update(shape=shape, dtype=operand.dtype,
                         weak_type=operand.weak_type),
          operand.update(shape=shape, dtype=np.dtype(np.int32)))

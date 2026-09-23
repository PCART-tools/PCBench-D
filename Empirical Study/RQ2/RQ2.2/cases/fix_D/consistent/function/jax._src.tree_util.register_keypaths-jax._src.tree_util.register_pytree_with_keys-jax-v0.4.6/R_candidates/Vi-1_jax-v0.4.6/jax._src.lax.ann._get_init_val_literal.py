def _get_init_val_literal(op_type, is_max_k):
  return np.array(np.NINF if is_max_k else np.Inf, dtype=op_type)

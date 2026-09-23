def bitcast_convert_type(operand, dtype):
  return np.asarray(operand).view(dtype)

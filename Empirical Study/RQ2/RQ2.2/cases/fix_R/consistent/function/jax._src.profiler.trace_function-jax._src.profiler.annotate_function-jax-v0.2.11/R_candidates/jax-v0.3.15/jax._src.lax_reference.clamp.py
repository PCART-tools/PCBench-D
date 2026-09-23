def clamp(min, operand, max):
  return np.clip(operand, np.clip(min, None, max), max).astype(operand.dtype)

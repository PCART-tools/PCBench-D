def reshape(operand, new_sizes, dimensions=None):
  if dimensions is None:
    dimensions = range(len(np.shape(operand)))
  return np.reshape(np.transpose(operand, dimensions), new_sizes)

def slice(operand, start_indices, limit_indices, strides=None):  # pylint: disable=redefined-builtin
  if strides is None:
    strides = np.ones(len(start_indices)).astype(int)
  slices = tuple(_map(_slice, start_indices, limit_indices, strides))
  return operand[slices]

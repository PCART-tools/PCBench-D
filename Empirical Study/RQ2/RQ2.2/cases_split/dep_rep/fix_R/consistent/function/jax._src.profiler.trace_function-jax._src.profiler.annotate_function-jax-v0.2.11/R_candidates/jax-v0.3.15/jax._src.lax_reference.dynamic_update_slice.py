def dynamic_update_slice(operand, update, start_indices):
  slices = tuple(_map(_slice, start_indices, np.add(start_indices, update.shape)))
  updated_operand = np.copy(operand)
  updated_operand[slices] = update
  return updated_operand

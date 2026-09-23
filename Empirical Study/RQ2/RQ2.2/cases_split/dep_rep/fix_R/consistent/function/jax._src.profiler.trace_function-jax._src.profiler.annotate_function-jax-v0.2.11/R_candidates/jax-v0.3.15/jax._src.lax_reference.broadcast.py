def broadcast(operand, sizes):
  return np.broadcast_to(operand, sizes + np.shape(operand))

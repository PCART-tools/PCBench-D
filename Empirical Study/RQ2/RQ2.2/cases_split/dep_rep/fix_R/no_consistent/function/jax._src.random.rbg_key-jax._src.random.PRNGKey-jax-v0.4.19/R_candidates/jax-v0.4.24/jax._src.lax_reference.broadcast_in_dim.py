def broadcast_in_dim(operand, shape, broadcast_dimensions):
  in_reshape = np.ones(len(shape), dtype=np.int32)
  for i, bd in enumerate(broadcast_dimensions):
    in_reshape[bd] = operand.shape[i]
  return np.broadcast_to(np.reshape(operand, in_reshape), shape)

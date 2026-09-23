def move_stacked_axis(operand, bdim, dst):
  dst = canonicalize_axis(dst, operand.ndim)
  if isinstance(bdim, int):
    return moveaxis(operand, bdim, dst), dst
  elif isinstance(bdim, RaggedAxis):
    result = moveaxis(operand, bdim.stacked_axis, dst)
    return result, bdim.move_stacked_axis(dst)
  else:
    raise TypeError(f"Unrecognized batch dimension type {bdim}")

def _merge_leading_axis(x, axis: Optional[int]):
  if axis is None:
    # We assume that the output does not vary along the leading axis
    return lax.index_in_dim(x, 0, axis=0, keepdims=False)
  else:
    x_moved = moveaxis(x, 0, axis)
    shape = list(x_moved.shape)
    shape[axis:axis + 2] = [shape[axis] * shape[axis + 1]]
    return x_moved.reshape(shape)

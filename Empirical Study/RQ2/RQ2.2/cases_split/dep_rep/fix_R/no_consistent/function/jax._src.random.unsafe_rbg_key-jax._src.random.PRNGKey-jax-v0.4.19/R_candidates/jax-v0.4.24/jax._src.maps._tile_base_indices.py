def _tile_base_indices(tile_shape, axes, axis_sizes):
  zero = np.zeros((), dtype=np.int32)
  linear_idxs = [zero] * len(tile_shape)
  strides = [1] * len(tile_shape)
  for name, axis in reversed(axes.items()):
    axis_index = lax.axis_index(name)
    stride_c = np.array(strides[axis], np.int32)
    if linear_idxs[axis] is zero and strides[axis] == 1:
      linear_idxs[axis] = axis_index
    else:
      linear_idxs[axis] = lax.add(linear_idxs[axis],
                                  lax.mul(axis_index, stride_c))
    strides[axis] *= axis_sizes[name]
  return [zero if linear_idx is zero else
          lax.mul(linear_idx, np.array(tile_dim_size, np.int32))
          for linear_idx, tile_dim_size in zip(linear_idxs, tile_shape)]

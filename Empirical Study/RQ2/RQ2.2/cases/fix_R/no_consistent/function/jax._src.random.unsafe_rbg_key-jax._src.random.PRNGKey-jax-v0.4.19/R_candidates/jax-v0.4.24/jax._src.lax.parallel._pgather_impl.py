def _pgather_impl(src, idx, *, axes):
  assert all(isinstance(axis, int) for axis in axes)
  src_axes_front = moveaxis(src, axes, range(len(axes)))
  non_axes_shape = src_axes_front.shape[len(axes):]
  src_one_axis_front = src_axes_front.reshape((-1,) + non_axes_shape)
  slice_sizes = (1,) + non_axes_shape
  idx = lax.expand_dims(idx, (-1,))
  offset_dims = tuple(range(idx.ndim - 1, idx.ndim + src_one_axis_front.ndim - 2))
  dnums = slicing.GatherDimensionNumbers(
      offset_dims=offset_dims,
      collapsed_slice_dims=(0,),
      start_index_map=(0,))
  return slicing.gather(src_one_axis_front, idx, dimension_numbers=dnums,
                        slice_sizes=tuple(slice_sizes))

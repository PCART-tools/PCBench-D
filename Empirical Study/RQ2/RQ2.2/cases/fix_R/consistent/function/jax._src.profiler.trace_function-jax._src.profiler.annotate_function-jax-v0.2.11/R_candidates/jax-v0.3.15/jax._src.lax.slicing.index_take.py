def index_take(src: Array, idxs: Array, axes: Sequence[int]) -> Array:
  indices = lax.concatenate([lax.expand_dims(i, (1,)) for i in idxs], 1)
  indices = indices % np.array([src.shape[ax] for ax in axes])
  slice_sizes = list(src.shape)
  for ax in axes:
    slice_sizes[ax] = 1
  offset_dims = tuple(range(1, src.ndim - indices.shape[1] + 1))
  dnums = GatherDimensionNumbers(
      offset_dims=offset_dims,
      collapsed_slice_dims=axes,
      start_index_map=axes)
  return gather(src, indices, dimension_numbers=dnums,
                slice_sizes=tuple(slice_sizes))

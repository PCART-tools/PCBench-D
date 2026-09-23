def _compute_pointers_from_indices(
    root_ptr: tc.tensor,
    block_info: BlockInfo | None,
    nd_indexer: NDIndexer,
    array_shape: tuple[int, ...],
) -> tc.tensor:
  if block_info is None:
    full_shape = array_shape
    num_mapped_dims = 0
    block_shape = array_shape
  else:
    full_shape = block_info.full_shape_dtype.shape
    num_mapped_dims = sum(
        b is pallas_core.mapped for b in block_info.block_shape
    )
    block_shape = block_info.block_shape
  strides = pallas_utils.strides_from_shape(full_shape)
  indexer_shape = nd_indexer.get_indexer_shape()
  int_indexer_shape = nd_indexer.int_indexer_shape
  indices = nd_indexer.indices
  other_shape = indexer_shape[len(int_indexer_shape) :]
  bcast_indices = []
  other_shape_idx = 0
  if block_info is None:
    start_index_offsets = [None] * len(indices)
  else:
    start_index_offsets = block_info.start_indices
  assert len(indices) + num_mapped_dims == len(full_shape)
  assert len(start_index_offsets) == len(full_shape)
  indexer_iter = iter(indices)
  for dim_stride, dim_block_size, start_offset in zip(
      strides, block_shape, start_index_offsets
  ):
    if dim_block_size is pallas_core.mapped:
      index = tc._to_tensor(0)
    else:
      index = next(indexer_iter)
    if isinstance(index, primitives.Slice):
      # Handle slices with static and dynamic indices and static sizes
      if isinstance(index.start, int):
        ptr_dim_offset = tc.arange(index.start, index.start + index.size)
      else:
        ptr_dim_offset = tc.semantic.add(
            tc.broadcast_to(index.start, [index.size]), tc.arange(0, index.size)
        )
      # We need to add broadcastable dimensions for the advanced int indexing
      # and for previous slices
      num_left_expand_dims = len(int_indexer_shape) + other_shape_idx
      num_right_expand_dims = len(other_shape) - other_shape_idx - 1
      other_shape_idx += 1
    elif isinstance(index, slice):
      if index != slice(None):
        raise NotImplementedError("Only `slice(None)` allowed.")
      ptr_dim_offset = tc.arange(0, dim_block_size)
      num_left_expand_dims = len(int_indexer_shape) + other_shape_idx
      num_right_expand_dims = len(other_shape) - other_shape_idx - 1
      other_shape_idx += 1
    else:
      # indexer is either a *scalar* or an array of size `int_indexer_shape`
      ptr_dim_offset = index
      num_left_expand_dims = 0
      num_right_expand_dims = len(other_shape)
      if not ptr_dim_offset.type.is_block():
        num_left_expand_dims = max(len(indexer_shape) - 1, 0)
      else:
        num_right_expand_dims = len(other_shape)
    if not ptr_dim_offset.type.is_block() and indexer_shape:
      ptr_dim_offset = tc.broadcast_to(
          ptr_dim_offset,
          [1] * len(indexer_shape),
      )
    else:
      for _ in range(num_left_expand_dims):
        ptr_dim_offset = tc.expand_dims(ptr_dim_offset, 0)
      for _ in range(num_right_expand_dims):
        ndim = len(ptr_dim_offset.shape)
        ptr_dim_offset = tc.expand_dims(ptr_dim_offset, ndim)
    if start_offset is not None:
      start_offset = tc.semantic.cast(start_offset, ptr_dim_offset.dtype)
      ptr_dim_offset = tc.semantic.add(
          ptr_dim_offset, tc.broadcast_to(start_offset, ptr_dim_offset.shape)
      )

    stride_size = tc.broadcast_to(
        tc._to_tensor(dim_stride, ptr_dim_offset.dtype), ptr_dim_offset.shape
    )
    bcast_indices.append(tc.semantic.mul(ptr_dim_offset, stride_size))
  block_shapes = [
      () if not index.type.is_block() else tuple(index.type.get_block_shapes())
      for index in bcast_indices
  ]
  bcast_indices = [
      tc.broadcast_to(index, indexer_shape)
      if indexer_shape != block_shape
      else index
      for index, block_shape in zip(bcast_indices, block_shapes)
  ]
  return functools.reduce(
      tc.semantic.add, bcast_indices, tc.broadcast_to(root_ptr, indexer_shape)
  )

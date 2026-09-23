def _compute_pointers_from_indices(
    root_ptr: tl.core.tensor,
    block_info: BlockInfo | None,
    nd_indexer: NDIndexer,
    array_shape: Tuple[int, ...],
    builder: tl_ir.builder,
) -> tl.core.tensor:
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
      index = tl.core._to_tensor(0, builder)
    else:
      index = next(indexer_iter)
    if isinstance(index, primitives.Slice):
      # Handle slices with static and dynamic indices and static sizes
      if isinstance(index.start, int):
        ptr_dim_offset = tl.arange(
            index.start, index.start + index.size, _builder=builder
        )
      else:
        ptr_dim_offset = index.start.__add__(
            tl.arange(0, index.size, _builder=builder), _builder=builder
        )
      # We need to add broadcastable dimensions for the advanced int indexing
      # and for previous slices
      num_left_expand_dims = len(int_indexer_shape) + other_shape_idx
      num_right_expand_dims = len(other_shape) - other_shape_idx - 1
      other_shape_idx += 1
    elif isinstance(index, slice):
      if index != slice(None):
        raise NotImplementedError("Only `slice(None)` allowed.")
      ptr_dim_offset = tl.arange(0, dim_block_size, _builder=builder)
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
      ptr_dim_offset = tl.broadcast_to(
          ptr_dim_offset,
          [tl.constexpr(1)] * len(indexer_shape),
          _builder=builder,
      )
    else:
      for _ in range(num_left_expand_dims):
        ptr_dim_offset = tl.semantic.expand_dims(ptr_dim_offset, 0, builder)
      for _ in range(num_right_expand_dims):
        ndim = len(ptr_dim_offset.shape)
        ptr_dim_offset = tl.semantic.expand_dims(ptr_dim_offset, ndim, builder)
    if start_offset is not None:
      ptr_dim_offset = ptr_dim_offset.__add__(start_offset, _builder=builder)
    stride_size = tl.core._to_tensor(int(dim_stride), builder)
    bcast_indices.append(ptr_dim_offset.__mul__(stride_size, _builder=builder))
  block_shapes = [
      () if not index.type.is_block() else tuple(index.type.get_block_shapes())
      for index in bcast_indices
  ]
  bcast_indices = [
      tl.core.broadcast_to(
          index, map(tl.constexpr, indexer_shape), _builder=builder
      )
      if indexer_shape != block_shape
      else index
      for index, block_shape in zip(bcast_indices, block_shapes)
  ]
  ptr = root_ptr
  for bcast_idx in bcast_indices:
    ptr = ptr.__add__(bcast_idx, _builder=builder)
  return ptr

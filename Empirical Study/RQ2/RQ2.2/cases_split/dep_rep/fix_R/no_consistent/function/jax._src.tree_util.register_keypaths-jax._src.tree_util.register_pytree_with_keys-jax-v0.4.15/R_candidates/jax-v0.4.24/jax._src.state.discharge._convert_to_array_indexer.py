def _convert_to_array_indexer(indexer: indexing.NDIndexer
                              ) -> tuple[int | Array, ...]:
  # This is the general gather case. We need to create the gather arrays.
  is_integer_indexer, _, integer_indexer = (
      indexing.unpack_ndindexer(indexer)
  )
  total_shape = indexer.get_indexer_shape()
  int_indexer_shape = indexer.int_indexer_shape
  slice_shape = total_shape[len(int_indexer_shape):]
  slice_dims = tuple(
      i + len(int_indexer_shape) for i in range(len(slice_shape))
  )
  slice_dim_iter = iter(slice_dims)
  slice_indexer: list[Array] = []
  for idx, is_int_index in zip(indexer.indices, is_integer_indexer):
    if not is_int_index:
      assert isinstance(idx, indexing.Slice)
      slice_indices = lax.broadcasted_iota(
          np.dtype("int32"), total_shape, next(slice_dim_iter)
      ) + idx.start
      slice_indexer.append(slice_indices)
      integer_indexer = tuple(
          lax.expand_dims(idx, (-1,)) for idx in integer_indexer
      )
      continue
  assert next(slice_dim_iter, None) is None
  return tuple(merge_lists(is_integer_indexer, slice_indexer, integer_indexer))

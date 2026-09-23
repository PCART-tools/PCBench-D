def _batch_indexer(indexer: indexing.NDIndexer, dims,
                   axis_size: int,
                   ref_shape: tuple[int, ...],
                   ref_dim: int | batching.NotMapped,
                   idx_is_batched: bool) -> indexing.NDIndexer:
  indices = indexer.indices
  indices_dims = dims.indices
  new_indices: list[Array | indexing.Slice | int] = []
  new_integer_indexer_shape = (axis_size, *indexer.int_indexer_shape)
  for idx, dim in zip(indices, indices_dims):
    if idx_is_batched:
      # If at least one of the idx is batched, we broadcast them all and move the
      # batch dim to the front.
      if isinstance(idx, indexing.Slice):
        # size is static, but start can be dynamic
        # Check if start is static (which it can be)
        is_static_slice = len(tree_util.tree_leaves(idx)) == 0
        if is_static_slice:
          new_indices.append(idx)
          continue
        dim = dim.start
        if dim is batching.not_mapped:
          # Broadcasting the slice is free (the start index stays the same)
          new_indices.append(idx)
        else:
          raise NotImplementedError(
              f"No support for vmapping over nontrivial slices just yet: {idx}")
      else:
        # Check if we are indexing with a scalar or not. If we are indexing
        # with a scalar and we are not batched, we can avoid broadcasting it.
        assert hasattr(idx, "shape")
        if not idx.shape:
          if dim is not batching.not_mapped:
            assert idx.shape == (axis_size,)
            idx = lax.broadcast_in_dim(idx, new_integer_indexer_shape, (0,))
          new_indices.append(idx)
        else:
          if dim is batching.not_mapped:
            bcast_dims = tuple(range(1, np.ndim(idx) + 1))
            idx = lax.broadcast_in_dim(idx, new_integer_indexer_shape,
                                       bcast_dims)
          else:
            idx = batching.moveaxis(idx, dim, 0)
          new_indices.append(idx)
    else:
      if ref_dim is not batching.not_mapped:
        if not isinstance(idx, indexing.Slice):
          assert hasattr(idx, "shape")
          if idx.shape:
            bcast_dims = tuple(range(1, np.ndim(idx) + 1))
            idx = lax.broadcast_in_dim(idx, new_integer_indexer_shape,
                                      bcast_dims)
      new_indices.append(idx)
  if ref_dim is not batching.not_mapped:
    iota = lax.broadcasted_iota(np.dtype('int32'), new_integer_indexer_shape, 0)
    new_indices.insert(ref_dim, iota)
  return indexing.NDIndexer(tuple(new_indices), ref_shape,
                            new_integer_indexer_shape,
                            validate=True)

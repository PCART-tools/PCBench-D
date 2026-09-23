  @classmethod
  def from_indices_shape(cls, indices, shape) -> NDIndexer:
    if not isinstance(indices, tuple):
      indices = (indices,)
    if len(indices) == 1 and indices[0] is ...:
      indices = (slice(None),) * len(shape)
    if any(idx is ... for idx in indices):
      # TODO(sharadmv,mattjj): support patterns that include ellipsis in them
      #                        e.g. x[0, ..., 1].
      raise NotImplementedError("Ellipsis in indexer not supported yet.")
    if len(indices) > len(shape):
      raise ValueError("`indices` must not be longer than `shape`: "
                       f"{indices=}, {shape=}")
    # Pad out indices with slice(None)
    indices = [*indices, *[slice(None)] * (len(shape) - len(indices))]
    # Convert all `slice`s to `Slice`s
    indices = tuple(Slice.from_slice(i, s) if isinstance(i, slice)
                    else i for i, s in zip(indices, shape))
    is_int_indexing = [not isinstance(i, Slice) for i in indices]
    other_indexers, int_indexers = partition_list(is_int_indexing, indices)
    indexer_shapes = [core.get_aval(i).shape for i in int_indexers]
    if indexer_shapes:
      try:
        bcast_shape = np.broadcast_shapes(*indexer_shapes)
      except ValueError as e:
        # Raise a nicer error than the NumPy one.
        raise ValueError("Cannot broadcast shapes for indexing: "
                         f"{tuple(a for a in indexer_shapes)}") from e
    else:
      bcast_shape = ()
    # Here we use the `broadcast_to` primitive instead of composing lax
    # primitives together because it is easier to lower in targets like
    # Triton/Mosaic.
    from jax._src.state import primitives as sp  # pytype: disable=import-error
    int_indexers = [sp.broadcast_to(i, bcast_shape) for i in int_indexers]
    indices = merge_lists(is_int_indexing, other_indexers, int_indexers)
    return NDIndexer(tuple(indices), shape, bcast_shape, validate=True)

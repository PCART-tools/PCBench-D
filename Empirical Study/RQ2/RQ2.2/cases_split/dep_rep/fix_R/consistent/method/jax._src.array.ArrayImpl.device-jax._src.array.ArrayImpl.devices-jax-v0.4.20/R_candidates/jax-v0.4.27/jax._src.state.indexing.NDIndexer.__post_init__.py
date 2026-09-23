  def __post_init__(self):
    if not self.validate:
      return
    if len(self.indices) != len(self.shape):
      raise ValueError(
          f"`indices` must be the same length as `Ref` shape.: {self}."
      )
    # We validate integer indexing shapes here
    for idx, s in zip(self.indices, self.shape):
      if isinstance(idx, Slice):
        start = idx.start
        if value := _maybe_concretize(start):
          if value >= s:
            raise ValueError(f"Out of bound slice: start={value}, dim={s}.")
          if size := _maybe_concretize(idx.size):
            if value + (size - 1) * idx.stride >= s:
              raise ValueError(
                  f"Out of bound slice: start={value}, size={size},"
                  f" stride={idx.stride}, dim={s}."
              )
        continue
      # The shape of indexer integers should be broadcastable up to the
      # int_indexer_shape of the whole NDIndexer
      if not np.shape(idx):
        if (value := _maybe_concretize(idx)) and value >= s:
          raise ValueError(f"Out of bound indexer: idx={value}, dim={s}.")
        # For ()-shaped indexers, we can broadcast no problm.
        continue
      # If we don't have a ()-shaped indexer, the rank must match
      # int_indexer_shape
      if np.ndim(idx) != len(self.int_indexer_shape):
        raise ValueError(
            f"Indexer must have rank {np.ndim(idx)}: {idx=} vs."
            f" {self.int_indexer_shape=}"
        )
      # Here we check that the shapes broadcast.
      try:
        np.broadcast_shapes(np.shape(idx), self.int_indexer_shape)
      except ValueError as e:
        raise ValueError(
            f"Could not broadcast integer indexer: {idx=} vs."
            f" {self.int_indexer_shape=}"
        ) from e

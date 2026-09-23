  def get_indexer_shape(self) -> tuple[int | Array, ...]:
    _, slice_indexers, _ = unpack_ndindexer(self)
    slice_shape = [s.size for s in slice_indexers]
    # In NDIndexers, the int_indexer_shape is *always* at the front of the
    # result.
    return (*self.int_indexer_shape, *slice_shape)

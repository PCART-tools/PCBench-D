def _index_ref(ref, ref_aval, ref_block_shape, indexers):
  for indexer in indexers:
    ref, ref_aval, ref_block_shape = _slice_memref(ref, ref_aval, indexer,
                                                   ref_block_shape)
  return ref, ref_aval, ref_block_shape

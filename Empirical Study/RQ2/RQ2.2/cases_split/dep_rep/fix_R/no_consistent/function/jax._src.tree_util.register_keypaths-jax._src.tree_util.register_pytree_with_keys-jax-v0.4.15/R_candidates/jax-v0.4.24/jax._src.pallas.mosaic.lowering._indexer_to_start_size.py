def _indexer_to_start_size(
    indexer: NDIndexer, ref_block_shape: tuple[int | pl_core.Mapped, ...], *,
    cast_to_index: bool,
) -> tuple[tuple[ir.Value, ...], tuple[int, ...], tuple[bool, ...],
           tuple[int | pl_core.Mapped, ...]]:
  indices_iter = iter(indexer.indices)
  starts, sizes, squeeze_dims = unzip3(
      (
          _maybe_cast_to_index(cast_to_index, 0),
          1,
          True,
      )
      if s is pl_core.mapped
      else _index_to_start_size(next(indices_iter), cast_to_index)
      for s in ref_block_shape
  )
  assert next(indices_iter, None) is None
  new_ref_block_shape = tuple(s for s, squeeze in zip(sizes, squeeze_dims)
                              if not squeeze)
  return tuple(starts), tuple(sizes), tuple(squeeze_dims), new_ref_block_shape

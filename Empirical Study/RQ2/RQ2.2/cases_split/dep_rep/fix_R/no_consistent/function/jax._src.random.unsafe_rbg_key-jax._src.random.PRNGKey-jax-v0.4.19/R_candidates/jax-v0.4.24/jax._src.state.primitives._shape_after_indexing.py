def _shape_after_indexing(
    shape: tuple[int, ...], indexers: tuple[indexing.NDIndexer, ...]
) -> tuple[int, ...]:
  for indexer in indexers:
    # Run some simple checks that all the indexers have consistent shapes
    assert indexer.shape == shape, (indexer.shape, shape)
    shape = indexer.get_indexer_shape()
  return shape

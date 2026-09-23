  @property
  def shape(self) -> tuple[int | Array, ...]:
    assert (
        len(self.indexers) > 0
    ), "Should not be able to create a trivial RefView"
    return self.indexers[-1].get_indexer_shape()

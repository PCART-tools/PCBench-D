@dataclasses.dataclass
class RefView:
  ref: Any
  indexers: tuple[indexing.NDIndexer, ...]

  @property
  def shape(self) -> tuple[int, ...]:
    assert (
        len(self.indexers) > 0
    ), "Should not be able to create a trivial RefView"
    return self.indexers[-1].get_indexer_shape()

  @property
  def dtype(self):
    return self.ref.dtype

  @property
  def at(self) -> RefIndexer:
    return RefIndexer(self)

  def __getattr__(self, name):
    return getattr(self.ref, name)

  def __getitem__(self, slc):
    from jax._src.state.primitives import ref_get  # pytype: disable=import-error
    return ref_get(self, slc)

  def __setitem__(self, slc, value):
    from jax._src.state.primitives import ref_set # pytype: disable=import-error
    return ref_set(self, slc, value)

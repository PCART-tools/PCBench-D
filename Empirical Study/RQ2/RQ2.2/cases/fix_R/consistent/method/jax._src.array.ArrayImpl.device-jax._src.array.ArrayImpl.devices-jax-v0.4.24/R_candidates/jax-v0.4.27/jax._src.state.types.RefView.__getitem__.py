  def __getitem__(self, slc):
    from jax._src.state.primitives import ref_get  # pytype: disable=import-error
    return ref_get(self, slc)

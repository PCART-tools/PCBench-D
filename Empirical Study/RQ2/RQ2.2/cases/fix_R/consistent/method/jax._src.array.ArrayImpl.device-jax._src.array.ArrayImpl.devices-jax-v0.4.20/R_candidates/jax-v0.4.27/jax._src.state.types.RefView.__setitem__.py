  def __setitem__(self, slc, value):
    from jax._src.state.primitives import ref_set # pytype: disable=import-error
    return ref_set(self, slc, value)

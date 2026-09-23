  def _getitem(self, tracer, idx) -> Array:
    from jax._src.state.primitives import ref_get  # pytype: disable=import-error
    return ref_get(tracer, idx)

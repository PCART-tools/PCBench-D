  @core.aval_method
  @staticmethod
  def set(tracer, value, idx=()):
    from jax._src.state.primitives import ref_set  # pytype: disable=import-error
    return ref_set(tracer, idx, value)

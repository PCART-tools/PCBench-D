  def __init__(self, inner_aval: jax_core.AbstractValue,
               memory_space: Any):
    assert isinstance(inner_aval, jax_core.ShapedArray)
    self.inner_aval = inner_aval
    self.memory_space = memory_space

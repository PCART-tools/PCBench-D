  @staticmethod
  def physical_element_aval(dtype) -> core.ShapedArray:
    return core.ShapedArray(dtype._impl.key_shape, jnp.dtype('uint32'))

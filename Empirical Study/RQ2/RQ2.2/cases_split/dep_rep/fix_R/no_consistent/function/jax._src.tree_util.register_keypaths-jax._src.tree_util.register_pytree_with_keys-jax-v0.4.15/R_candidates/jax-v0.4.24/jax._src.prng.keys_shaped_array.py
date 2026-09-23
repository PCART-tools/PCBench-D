def keys_shaped_array(impl, shape):
  return core.ShapedArray(shape, KeyTy(impl))

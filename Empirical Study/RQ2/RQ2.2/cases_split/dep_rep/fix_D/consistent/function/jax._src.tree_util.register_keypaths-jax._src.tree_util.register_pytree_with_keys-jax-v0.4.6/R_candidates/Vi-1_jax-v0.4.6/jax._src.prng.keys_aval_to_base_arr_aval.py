def keys_aval_to_base_arr_aval(keys_aval):
  shape = (*keys_aval.shape, *keys_aval.dtype.impl.key_shape)
  return core.ShapedArray(shape, np.dtype('uint32'))

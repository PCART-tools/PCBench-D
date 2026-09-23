def _dynamic_array_result_handler(sticky_device, aval, env, buf):
  in_env, out_env = env or (None, None)
  shape = [in_env[d.val] if type(d) is core.InDBIdx else
           out_env[d.val] if type(d) is core.OutDBIdx else d
           for d in aval.shape]
  if all(type(d) is int for d in shape):
    aval = core.ShapedArray(tuple(shape), aval.dtype)
    return _maybe_create_array_from_da(buf, aval, sticky_device)
  elif any(type(d) is core.BInt for d in shape):
    padded_shape = [d.bound if type(d) is core.BInt else d for d in shape]
    buf_aval = core.ShapedArray(tuple(padded_shape), aval.dtype, aval.weak_type)
    data = _maybe_create_array_from_da(buf, buf_aval, sticky_device)
    return core.PaddedArray(aval.update(shape=tuple(shape)), data)
  else:
    aval = core.ShapedArray(tuple(shape), aval.dtype)
    return _maybe_create_array_from_da(buf, aval, sticky_device)

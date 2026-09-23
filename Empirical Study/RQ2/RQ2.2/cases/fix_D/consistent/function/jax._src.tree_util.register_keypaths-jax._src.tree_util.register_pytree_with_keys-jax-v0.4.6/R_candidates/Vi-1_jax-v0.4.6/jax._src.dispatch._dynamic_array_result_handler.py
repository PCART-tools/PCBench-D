def _dynamic_array_result_handler(sticky_device, aval, env, buf):
  in_env, out_env = env or (None, None)
  shape = [in_env[d.val] if type(d) is core.InDBIdx else
           out_env[d.val] if type(d) is core.OutDBIdx else d
           for d in aval.shape]
  if all(type(d) is int for d in shape) and type(aval.dtype) is not core.bint:
    aval = core.ShapedArray(tuple(shape), buf.dtype)
    return maybe_create_array_from_da(buf, aval, sticky_device)
  else:
    pad_shape = [d.dtype.bound if _is_bint_axis_size(d) else d for d in shape]
    buf_aval = core.ShapedArray(tuple(pad_shape), buf.dtype, aval.weak_type)
    data = maybe_create_array_from_da(buf, buf_aval, sticky_device)
    return core.DArray(aval.update(shape=tuple(shape)), data)

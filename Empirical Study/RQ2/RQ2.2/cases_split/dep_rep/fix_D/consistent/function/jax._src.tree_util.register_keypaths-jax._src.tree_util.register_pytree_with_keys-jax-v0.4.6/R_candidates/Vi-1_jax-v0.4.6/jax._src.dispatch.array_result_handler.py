def array_result_handler(sticky_device: Optional[Device],
                         aval: core.ShapedArray):
  if not core.is_opaque_dtype(aval.dtype) and aval.dtype == dtypes.float0:
    return lambda _, __: np.zeros(aval.shape, dtypes.float0)
  aval = core.raise_to_shaped(aval)
  if core.is_opaque_dtype(aval.dtype):
    return aval.dtype._rules.result_handler(sticky_device, aval)
  handler = lambda _, b: maybe_create_array_from_da(b, aval, sticky_device)
  handler.args = aval, sticky_device  # for C++ dispatch path in api.py
  return handler

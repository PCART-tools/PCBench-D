def array_result_handler(sticky_device: Optional[Device],
                         aval: core.ShapedArray):
  if aval.dtype == dtypes.float0:
    return lambda _, __: np.zeros(aval.shape, dtypes.float0)
  aval = core.raise_to_shaped(aval)
  handler = lambda _, b: _maybe_create_array_from_da(b, aval, sticky_device)
  handler.args = aval, sticky_device  # for C++ dispatch path in api.py
  return handler

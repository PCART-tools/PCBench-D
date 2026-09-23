def _set_device_array_base_attributes(device_array):
  # Forward operators, methods, and properties on DeviceArray to lax_numpy
  # functions (with no Tracers involved; this forwarding is direct)
  for operator_name, function in _operators.items():
    setattr(device_array, f"__{operator_name}__", function)
  for method_name in _nondiff_methods + _diff_methods:
    setattr(device_array, method_name, globals()[method_name])
  # TODO(jakevdp): remove tile method after August 2022
  setattr(device_array, "tile", _deprecate_function(tile, "arr.tile(...) is deprecated and will be removed. Use jnp.tile(arr, ...) instead."))
  setattr(device_array, "reshape", _reshape)
  setattr(device_array, "transpose", _transpose)
  setattr(device_array, "flatten", ravel)
  setattr(device_array, "flat", property(_notimplemented_flat))
  setattr(device_array, "T", property(transpose))
  setattr(device_array, "real", property(real))
  setattr(device_array, "imag", property(imag))
  setattr(device_array, "astype", _astype)
  setattr(device_array, "view", _view)
  setattr(device_array, "nbytes", property(_nbytes))
  setattr(device_array, "itemsize", property(_itemsize))
  setattr(device_array, "clip", _clip)

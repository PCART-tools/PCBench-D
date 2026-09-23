def _set_shaped_array_attributes(shaped_array):
  # Set up operator, method, and property forwarding on Tracer instances
  # containing
  # ShapedArray avals by following the forwarding conventions for Tracer.
  # Forward operators using a single-underscore-prefix naming convention:
  for operator_name, function in _operators.items():
    setattr(shaped_array, f"_{operator_name}", staticmethod(function))
  # Forward methods and properties using core.{aval_method, aval_property}:
  for method_name in _nondiff_methods + _diff_methods:
    setattr(shaped_array, method_name, core.aval_method(globals()[method_name]))
  # TODO(jakevdp): remove tile method after August 2022
  setattr(shaped_array, "tile", core.aval_method(_deprecate_function(tile, "arr.tile(...) is deprecated and will be removed. Use jnp.tile(arr, ...) instead.")))
  setattr(shaped_array, "reshape", core.aval_method(_reshape))
  setattr(shaped_array, "transpose", core.aval_method(_transpose))
  setattr(shaped_array, "flatten", core.aval_method(ravel))
  setattr(shaped_array, "flat", core.aval_property(_notimplemented_flat))
  setattr(shaped_array, "T", core.aval_property(transpose))
  setattr(shaped_array, "real", core.aval_property(real))
  setattr(shaped_array, "imag", core.aval_property(imag))
  setattr(shaped_array, "astype", core.aval_method(_astype))
  setattr(shaped_array, "view", core.aval_method(_view))
  setattr(shaped_array, "nbytes", core.aval_property(_nbytes))
  setattr(shaped_array, "itemsize", core.aval_property(_itemsize))
  setattr(shaped_array, "clip", core.aval_method(_clip))

  setattr(shaped_array, "_array_module", staticmethod(__array_module__))
  setattr(shaped_array, "broadcast", core.aval_method(lax.broadcast))
  setattr(shaped_array, "broadcast_in_dim", core.aval_method(lax.broadcast_in_dim))
  setattr(shaped_array, "split", core.aval_method(split))
  setattr(shaped_array, "compress", _compress_method)
  setattr(shaped_array, "at", core.aval_property(_IndexUpdateHelper))
  setattr(shaped_array, "item", core.aval_method(device_array.DeviceArray.item))

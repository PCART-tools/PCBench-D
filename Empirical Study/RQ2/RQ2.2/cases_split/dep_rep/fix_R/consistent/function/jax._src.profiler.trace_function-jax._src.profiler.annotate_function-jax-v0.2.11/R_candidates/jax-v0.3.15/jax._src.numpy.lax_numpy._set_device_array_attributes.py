def _set_device_array_attributes(device_array):
  setattr(device_array, "__array_module__", __array_module__)
  # Extra methods that are handy
  setattr(device_array, "broadcast", lax.broadcast)
  setattr(device_array, "broadcast_in_dim", lax.broadcast_in_dim)
  setattr(device_array, "split", split)
  setattr(device_array, "compress", _compress_method)
  setattr(device_array, "_multi_slice", _multi_slice)
  setattr(device_array, "at", property(_IndexUpdateHelper))

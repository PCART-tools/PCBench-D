def register_jax_array_methods():
  """Call this function once to register methods of JAX arrays"""
  _set_shaped_array_attributes(core.ShapedArray)
  _set_shaped_array_attributes(core.DShapedArray)

  _set_device_array_base_attributes(device_array.DeviceArray)
  _set_device_array_base_attributes(ArrayImpl, exclude={'__getitem__'})

  for t in device_array.device_array_types:
    _set_device_array_attributes(t)
    _set_device_array_attributes(ArrayImpl)

  Array.at.__doc__ = _IndexUpdateHelper.__doc__

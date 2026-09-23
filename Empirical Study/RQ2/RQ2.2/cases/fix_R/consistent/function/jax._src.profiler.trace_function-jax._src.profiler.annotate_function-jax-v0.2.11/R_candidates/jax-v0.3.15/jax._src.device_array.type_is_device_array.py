def type_is_device_array(x):
  """Returns `True` if `x` is a non-sharded DeviceArray.

  Use this function instead of `type(x) is Devicearray`.
  """
  type_x = type(x)
  return type_x is _DeviceArray or type_x is xc.Buffer

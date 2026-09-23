def device_array_supports_weakrefs():
  try:
    weakref.ref(DeviceArray())
    return True
  except TypeError:
    return False

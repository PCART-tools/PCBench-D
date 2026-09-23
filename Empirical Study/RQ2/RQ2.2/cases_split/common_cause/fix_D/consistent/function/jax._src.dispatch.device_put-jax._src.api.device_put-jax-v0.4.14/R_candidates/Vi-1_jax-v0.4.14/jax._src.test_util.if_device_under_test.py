def if_device_under_test(device_type: Union[str, Sequence[str]],
                         if_true, if_false):
  """Chooses `if_true` of `if_false` based on device_under_test."""
  if device_under_test() in ([device_type] if isinstance(device_type, str)
                             else device_type):
    return if_true
  else:
    return if_false

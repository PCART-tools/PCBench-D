def _get_device(a: ArrayImpl) -> Device:
  assert len(a.devices()) == 1
  return next(iter(a.devices()))

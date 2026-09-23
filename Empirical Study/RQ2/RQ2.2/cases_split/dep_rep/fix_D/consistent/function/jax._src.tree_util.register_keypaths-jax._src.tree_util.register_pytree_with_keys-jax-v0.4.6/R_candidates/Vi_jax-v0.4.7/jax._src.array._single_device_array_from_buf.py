def _single_device_array_from_buf(buf, committed) -> ArrayImpl:
  if isinstance(buf, ArrayImpl) and buf._committed == committed:  # type: ignore
    return buf
  db = dispatch._set_aval(buf)
  return ArrayImpl(db.aval, SingleDeviceSharding(db.device()), [db],
                   committed=committed, _skip_checks=True)

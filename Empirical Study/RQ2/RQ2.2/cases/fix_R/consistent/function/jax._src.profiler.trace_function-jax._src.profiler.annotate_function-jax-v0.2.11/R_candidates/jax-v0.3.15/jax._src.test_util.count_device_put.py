@contextmanager
def count_device_put():
  device_put = dispatch.device_put
  count = [0]

  def device_put_and_count(*args, **kwargs):
    count[0] += 1
    return device_put(*args, **kwargs)

  dispatch.device_put = device_put_and_count
  try:
    yield count
  finally:
    dispatch.device_put = device_put

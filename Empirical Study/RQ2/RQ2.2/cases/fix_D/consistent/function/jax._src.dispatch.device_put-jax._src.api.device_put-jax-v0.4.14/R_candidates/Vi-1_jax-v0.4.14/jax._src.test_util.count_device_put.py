@contextmanager
def count_device_put():
  batched_device_put = pxla.batched_device_put
  count = [0]

  def make_fn_and_count(fn):
    def fn_and_count(*args, **kwargs):
      count[0] += 1
      # device_put handlers might call `dispatch.device_put` (e.g. on an
      # underlying payload or several). We only want to count these
      # recursive puts once, so we skip counting more than the outermost
      # one in such a call stack.
      pxla.batched_device_put = batched_device_put
      try:
        return fn(*args, **kwargs)
      finally:
        pxla.batched_device_put = batched_device_put_and_count
    return fn_and_count

  batched_device_put_and_count = make_fn_and_count(batched_device_put)

  pxla.batched_device_put = batched_device_put_and_count
  try:
    yield count
  finally:
    pxla.batched_device_put = batched_device_put

  def batched_device_put(aval, sharding, xs, devices, committed=True):
    return [d.client.buffer_from_pyval(x, d) for x, d in safe_zip(xs, devices)]

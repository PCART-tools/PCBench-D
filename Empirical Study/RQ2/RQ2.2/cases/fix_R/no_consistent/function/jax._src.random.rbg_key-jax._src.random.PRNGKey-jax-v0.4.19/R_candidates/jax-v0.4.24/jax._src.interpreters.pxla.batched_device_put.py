def batched_device_put(aval: core.ShapedArray,
                       sharding: jax.sharding.Sharding, xs: Sequence[Any],
                       devices: Sequence[jax.Device], committed: bool = True):
  from jax._src import array

  bufs = [x for x, d in safe_zip(xs, devices)
          if (isinstance(x, array.ArrayImpl) and
              dispatch.is_single_device_sharding(x.sharding) and
              x.devices() == {d})]
  if len(bufs) == len(xs):
    return array.ArrayImpl(
        aval, sharding, bufs, committed=committed, _skip_checks=True)
  return xc.batched_device_put(aval, sharding, xs, list(devices), committed)  # type: ignore

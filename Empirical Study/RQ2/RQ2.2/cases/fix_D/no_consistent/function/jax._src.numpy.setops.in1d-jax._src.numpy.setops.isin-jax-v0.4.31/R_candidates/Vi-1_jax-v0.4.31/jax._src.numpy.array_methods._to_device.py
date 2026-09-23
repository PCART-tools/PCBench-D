def _to_device(arr: ArrayLike, device: xc.Device | Sharding, *,
               stream: int | Any | None = None):
  if stream is not None:
    raise NotImplementedError("stream argument of array.to_device()")
  return api.device_put(arr, device)

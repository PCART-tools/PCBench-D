def _to_device(self: Array, device: xc.Device | Sharding, *,
               stream: int | Any | None = None):
  """Return a copy of the array on the specified device

  Args:
    device: :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.
    stream: not implemented, passing a non-None value will lead to an error.
  Returns:
    copy of array placed on the specified device or devices.
  """
  if stream is not None:
    raise NotImplementedError("stream argument of array.to_device()")
  return api.device_put(self, device)

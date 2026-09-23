  def __dlpack__(self, *, stream: int | Any | None = None,
                 max_version: tuple[int, int] | None = None,
                 dl_device: tuple[DLDeviceType, int] | None = None,
                 copy: bool | None = None):
    from jax._src.dlpack import to_dlpack  # pylint: disable=g-import-not-at-top

    device_set = self.sharding.device_set
    if len(device_set) > 1:
      raise BufferError(
        "to_dlpack can only pack a dlpack tensor from an array on a singular "
        f"device, but an array with a Sharding over {len(device_set)} devices "
        "was provided."
      )
    device, = device_set
    return to_dlpack(self, stream=stream,
                     max_version=max_version,
                     src_device=device,
                     dl_device=dl_device,
                     copy=copy)

  def __dlpack_device__(self) -> tuple[enum.Enum, int]:
    if len(self._arrays) != 1:
      raise BufferError("__dlpack__ only supported for unsharded arrays.")

    from jax._src.dlpack import DLDeviceType  # pylint: disable=g-import-not-at-top

    if self.platform() == "cpu":
      return DLDeviceType.kDLCPU, 0

    elif self.platform() == "gpu":
      platform_version = _get_device(self).client.platform_version
      if "cuda" in platform_version:
        dl_device_type = DLDeviceType.kDLCUDA
      elif "rocm" in platform_version:
        dl_device_type = DLDeviceType.kDLROCM
      else:
        raise BufferError("Unknown GPU platform for __dlpack__: "
                         f"{platform_version}")

      local_hardware_id = _get_device(self).local_hardware_id
      if local_hardware_id is None:
        raise BufferError("Couldn't get local_hardware_id for __dlpack__")

      return dl_device_type, local_hardware_id

    else:
      raise BufferError(
          "__dlpack__ device only supported for CPU and GPU, got platform: "
          f"{self.platform()}"
      )

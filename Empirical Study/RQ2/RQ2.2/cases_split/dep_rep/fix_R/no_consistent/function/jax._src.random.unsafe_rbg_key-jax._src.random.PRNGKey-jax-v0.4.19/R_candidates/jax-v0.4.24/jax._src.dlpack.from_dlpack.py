def from_dlpack(external_array):
  """Returns a :class:`~jax.Array` representation of a DLPack tensor.

  The returned :class:`~jax.Array` shares memory with ``external_array``.

  Args:
    external_array: an array object that has __dlpack__ and __dlpack_device__
      methods, or a DLPack tensor on either CPU or GPU (legacy API).

  Returns:
    A jax.Array

  Note:
    While JAX arrays are always immutable, dlpack buffers cannot be marked as
    immutable, and it is possible for processes external to JAX to mutate them
    in-place. If a jax Array is constructed from a dlpack buffer and the buffer
    is later modified in-place, it may lead to undefined behavior when using
    the associated JAX array.
  """
  if hasattr(external_array, "__dlpack__"):
    dl_device_type, device_id = external_array.__dlpack_device__()
    try:
      device_platform = {
          DLDeviceType.kDLCPU: "cpu",
          DLDeviceType.kDLCUDA: "cuda",
          DLDeviceType.kDLROCM: "rocm",
      }[dl_device_type]
    except TypeError:
      # https://dmlc.github.io/dlpack/latest/python_spec.html recommends using
      # TypeError.
      raise TypeError(
          "Array passed to from_dlpack is on unsupported device type "
          f"(DLDeviceType: {dl_device_type}, array: {external_array}")

    backend = xla_bridge.get_backend(device_platform)
    device = backend.device_from_local_hardware_id(device_id)
    try:
      stream = device.get_stream_for_external_ready_events()
    except xla_client.XlaRuntimeError as err:  # type: ignore
      if "UNIMPLEMENTED" in str(err):
        stream = None
      else:
        raise
    dlpack = external_array.__dlpack__(stream=stream)

    return jnp.asarray(xla_client._xla.dlpack_managed_tensor_to_buffer(
        dlpack, device, stream))
  else:
    # Legacy path
    dlpack = external_array
    cpu_backend = xla_bridge.get_backend("cpu")
    try:
      gpu_backend = xla_bridge.get_backend("cuda")
    except RuntimeError:
      gpu_backend = None

    # Try ROCm if CUDA backend not found
    if gpu_backend is None:
      try:
        gpu_backend = xla_bridge.get_backend("rocm")
      except RuntimeError:
        gpu_backend = None

    return jnp.asarray(xla_client._xla.dlpack_managed_tensor_to_buffer(
        dlpack, cpu_backend, gpu_backend))

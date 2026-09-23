def from_dlpack(dlpack):
  """Returns a ``DeviceArray`` representation of a DLPack tensor.

  The returned ``DeviceArray`` shares memory with ``dlpack``.

  Args:
    dlpack: a DLPack tensor, on either CPU or GPU.
  """
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

  if xla_extension_version >= 140:
    return jnp.asarray(xla_client._xla.dlpack_managed_tensor_to_buffer(
        dlpack, cpu_backend, gpu_backend))
  else:
    buf = xla_client._xla.dlpack_managed_tensor_to_buffer(
        dlpack, cpu_backend, gpu_backend)
    if isinstance(buf, array.ArrayImpl):
      return jnp.asarray(buf)  # asarray ensures dtype canonicalization
    else:
      return jnp.asarray(array._single_device_array_from_buf(
          buf, committed=buf.device() is not None))

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
  buf = xla_client._xla.dlpack_managed_tensor_to_buffer(
      dlpack, cpu_backend, gpu_backend)

  xla_shape = buf.xla_shape()
  assert not xla_shape.is_tuple()
  aval = core.ShapedArray(xla_shape.dimensions(), xla_shape.numpy_dtype())
  return device_array.make_device_array(aval, buf.device(), buf)  # pytype: disable=attribute-error

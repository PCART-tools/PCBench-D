class _DeviceArray(DeviceArray):  # type: ignore
  """A DeviceArray is an ndarray backed by a single device memory buffer."""
  # We don't subclass ndarray because that would open up a host of issues,
  # but lax_numpy.py overrides isinstance behavior and attaches ndarray methods.
  __slots__ = [
      "aval", "device_buffer", "_npy_value", "_device", "__weakref__"
  ]
  __array_priority__ = 100

  # DeviceArray has methods that are dynamically populated in lax_numpy.py,
  # and this annotation is needed to make pytype happy.
  _HAS_DYNAMIC_ATTRIBUTES = True

  def __init__(self, aval: core.ShapedArray, device: Optional[Device],
               device_buffer: Buffer):
    """Initializer.

    Args:
      aval: The abstract value associated to this array (shape+dtype+weak_type).
      device:  The optional sticky device. See
        https://jax.readthedocs.io/en/latest/faq.html#controlling-data-and-computation-placement-on-devices
      device_buffer: The underlying buffer owning the on-device data.
    """
    DeviceArray.__init__(self)
    self.aval = aval
    self.device_buffer = device_buffer
    self._device = device

    self._npy_value = None
    if config.jax_enable_checks:
      assert type(aval) is core.ShapedArray
      npy_value = self._value
      assert npy_value.dtype == aval.dtype and npy_value.shape == aval.shape, (
          aval, npy_value.shape, npy_value.dtype)
      assert (device is None) or device is device_buffer.device()

  def _check_if_deleted(self):
    if self.device_buffer is deleted_buffer:
      raise RuntimeError("DeviceArray has been deleted.")

  @profiler.annotate_function
  def block_until_ready(self):
    """Blocks the caller until the buffer's value has been computed on device.

    This method is mostly useful for timing microbenchmarks that wish to
    time how long a computation takes, without transferring the result back
    to the host.

    Returns the buffer object (`self`).
    """
    self._check_if_deleted()
    self.device_buffer.block_until_ready()
    return self

  @property
  def _value(self):
    self._check_if_deleted()
    if self._npy_value is None:
      self._npy_value = self.device_buffer.to_py()  # pytype: disable=attribute-error  # bind-properties
      self._npy_value.flags.writeable = False
    return self._npy_value

  @property
  def shape(self):
    return self.aval.shape

  @property
  def dtype(self):
    return self.aval.dtype

  @property
  def size(self):
    return util.prod(self.aval.shape)

  @property
  def ndim(self):
    return len(self.aval.shape)

  def device(self):
    self._check_if_deleted()
    return self.device_buffer.device()  # pytype: disable=attribute-error

  def copy_to_host_async(self):
    """Requests a copy of the buffer to the host."""
    self._check_if_deleted()
    if self._npy_value is None:
      self.device_buffer.copy_to_host_async()  # pytype: disable=attribute-error

  def delete(self):
    """Deletes the device array and any cached copy on the host.

    It is an error to access the contents of a `DeviceArray` after it has
    been deleted.

    Use of this method is optional; device buffers will be reclaimed
    automatically by Python when a DeviceArray object is garbage collected.
    However, it is sometimes useful to have more explicit control over the
    time of deletion.
    """
    self.device_buffer.delete()  # pytype: disable=attribute-error
    self.device_buffer = deleted_buffer
    self._npy_value = None

  @property
  def __cuda_array_interface__(self):
    return self.device_buffer.__cuda_array_interface__  # pytype: disable=attribute-error  # bind-properties

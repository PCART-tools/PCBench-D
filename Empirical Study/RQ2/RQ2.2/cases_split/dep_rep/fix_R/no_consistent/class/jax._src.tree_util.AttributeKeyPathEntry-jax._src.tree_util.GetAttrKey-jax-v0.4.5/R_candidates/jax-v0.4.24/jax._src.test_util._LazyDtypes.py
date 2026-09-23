class _LazyDtypes:
  """A class that unifies lists of supported dtypes.

  These could be module-level constants, but device_under_test() is not always
  known at import time, so we need to define these lists lazily.
  """
  def supported(self, dtypes):
    supported = supported_dtypes()
    return type(dtypes)(d for d in dtypes if d in supported)

  @_cached_property
  def custom_floats(self):
    return [np.dtype(t) for t in [
      _dtypes.bfloat16, _dtypes.float8_e4m3b11fnuz,
      _dtypes.float8_e4m3fn, _dtypes.float8_e4m3fnuz,
      _dtypes.float8_e5m2, _dtypes.float8_e5m2fnuz]]

  @_cached_property
  def floating(self):
    return self.supported([np.float32, np.float64])

  @_cached_property
  def all_floating(self):
    return self.supported([_dtypes.bfloat16, np.float16, np.float32, np.float64])

  @_cached_property
  def integer(self):
    return self.supported([np.int32, np.int64])

  @_cached_property
  def all_integer(self):
    return self.supported([np.int8, np.int16, np.int32, np.int64])

  @_cached_property
  def unsigned(self):
    return self.supported([np.uint32, np.uint64])

  @_cached_property
  def all_unsigned(self):
    return self.supported([np.uint8, np.uint16, np.uint32, np.uint64])

  @_cached_property
  def complex(self):
    return self.supported([np.complex64, np.complex128])

  @_cached_property
  def boolean(self):
    return self.supported([np.bool_])

  @_cached_property
  def inexact(self):
    return self.floating + self.complex

  @_cached_property
  def all_inexact(self):
    return self.all_floating + self.complex

  @_cached_property
  def numeric(self):
    return self.floating + self.integer + self.unsigned + self.complex

  @_cached_property
  def all(self):
    return (self.all_floating + self.all_integer + self.all_unsigned +
            self.complex + self.boolean)

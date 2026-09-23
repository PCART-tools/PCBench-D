  def __array__(self, *args, **kw):
    raise TracerArrayConversionError(self)

  def str_short(self, short_dtypes=False) -> str:
    return _short_dtype_name(self.dtype) if short_dtypes else self.dtype.name

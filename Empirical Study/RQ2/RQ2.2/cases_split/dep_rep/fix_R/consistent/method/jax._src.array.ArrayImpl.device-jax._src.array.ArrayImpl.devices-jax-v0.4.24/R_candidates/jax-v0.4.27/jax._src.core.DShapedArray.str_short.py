  def str_short(self, short_dtypes=False) -> str:
    del short_dtypes  # ignored
    shape = f'{",".join(str(d) for d in self.shape)}' if self.shape else ''
    dtype = _short_dtype_name(self.dtype)
    return f'{dtype}[{shape}]'

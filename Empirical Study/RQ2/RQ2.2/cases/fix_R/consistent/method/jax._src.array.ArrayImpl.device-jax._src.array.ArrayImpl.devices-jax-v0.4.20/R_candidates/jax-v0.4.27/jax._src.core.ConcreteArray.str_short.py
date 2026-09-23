  def str_short(self, short_dtypes=False) -> str:
    dt_str =  _short_dtype_name(self.dtype) if short_dtypes else self.dtype.name
    return f'{self.val}, dtype={dt_str}'

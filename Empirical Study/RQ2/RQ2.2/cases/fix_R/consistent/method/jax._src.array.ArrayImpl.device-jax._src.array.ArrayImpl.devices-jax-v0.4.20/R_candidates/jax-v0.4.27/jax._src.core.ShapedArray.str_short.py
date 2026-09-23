  def str_short(self, short_dtypes=False):
    dt_str =  _short_dtype_name(self.dtype) if short_dtypes else self.dtype.name
    shapestr = ','.join(map(str, self.shape))
    if self.named_shape:
      named_shapestr = ','.join(f'{k}:{v}' for k, v in self.named_shape.items())
      return f'{dt_str}[{shapestr};{named_shapestr}]'
    else:
      return f'{dt_str}[{shapestr}]'

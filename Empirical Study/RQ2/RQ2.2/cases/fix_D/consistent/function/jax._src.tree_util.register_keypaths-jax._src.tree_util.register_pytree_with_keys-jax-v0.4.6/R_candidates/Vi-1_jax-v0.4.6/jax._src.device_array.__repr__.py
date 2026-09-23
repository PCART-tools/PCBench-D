  def __repr__(self):
    line_width = np.get_printoptions()["linewidth"]
    prefix = '{}('.format(self.__class__.__name__.lstrip('_'))
    s = np.array2string(self._value, prefix=prefix, suffix=',',
                        separator=', ', max_line_width=line_width)
    if self.aval is not None and self.aval.weak_type:
      dtype_str = f'dtype={self.dtype.name}, weak_type=True)'
    else:
      dtype_str = f'dtype={self.dtype.name})'
    last_line_len = len(s) - s.rfind('\n') + 1
    sep = ' '
    if last_line_len + len(dtype_str) + 1 > line_width:
      sep = ' ' * len(prefix)
    return f"{prefix}{s},{sep}{dtype_str}"

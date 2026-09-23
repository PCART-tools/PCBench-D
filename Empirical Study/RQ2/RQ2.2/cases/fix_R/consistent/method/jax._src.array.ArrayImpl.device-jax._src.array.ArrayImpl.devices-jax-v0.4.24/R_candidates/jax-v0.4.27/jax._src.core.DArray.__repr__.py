  def __repr__(self) -> str:
    if not self.shape and type(self.dtype) is bint:
      # special-case scalar bints
      return f'{int(self._data)}{{≤{self.dtype.bound}}}'

    dtypestr = _short_dtype_name(self._aval.dtype)
    shapestr = ','.join(map(str, self.shape))
    slices = tuple(slice(int(d._data)) if type(d) is DArray and
                   type(d.dtype) is bint else slice(None) for d in self.shape)
    data = self._data[slices]
    return f'{dtypestr}[{shapestr}] with value: {data}'

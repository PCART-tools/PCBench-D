class DArray:
  _aval: DShapedArray
  _data: Any  # standard array type
  def __init__(self, aval, data):
    pad_shape = tuple(d.dtype.bound if type(d) is DArray and
                      type(d.dtype) is bint else d for d in aval.shape)
    assert data.shape == pad_shape
    self._aval = aval
    self._data = data
  shape = property(lambda self: self._aval.shape)
  dtype = property(lambda self: self._aval.dtype)
  aval = property(lambda self: self._aval)
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
  def __hash__(self) -> int:
    if not self.shape:
      return hash((self._aval, int(self._data)))
    raise TypeError("unhashable type: DArray")
  def __eq__(self, other):
    if isinstance(other, DArray) and self._aval == other._aval:
      return self._data == other._data
    return False
  def __len__(self):
    return self.shape[0]

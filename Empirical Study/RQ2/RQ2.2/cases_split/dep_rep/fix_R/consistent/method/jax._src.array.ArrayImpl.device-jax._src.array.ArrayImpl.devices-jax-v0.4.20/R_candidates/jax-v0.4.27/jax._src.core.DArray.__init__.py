  def __init__(self, aval, data):
    pad_shape = tuple(d.dtype.bound if type(d) is DArray and
                      type(d.dtype) is bint else d for d in aval.shape)
    assert data.shape == pad_shape
    self._aval = aval
    self._data = data

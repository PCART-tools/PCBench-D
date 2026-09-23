  def __repr__(self) -> str:
    cls_name = self.__class__.__name__
    ids = self._ids.copy()
    platform_name = self._devices[0].platform.upper()
    for idx, x in np.ndenumerate(ids):
      ids[idx] = DeviceIdSet(platform_name, *(self._devices[i].id for i in x))
    body = np.array2string(ids, prefix=cls_name + '(', suffix=')',
                           max_line_width=100)
    mem = '' if self._memory_kind is None else f', memory_kind={self._memory_kind}'
    return f'{cls_name}({body}{mem}, shape={self.shape})'

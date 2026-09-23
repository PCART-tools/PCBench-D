  def __getitem__(self, idx):
    try:
      idx = operator.index(idx)
      return self.__positional[idx]
    except TypeError:
      pass
    return self.__named[idx]

  @property
  def rank(self):
    return len(self.__positional) + len(self.__named)

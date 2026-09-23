  def __eq__(self, other):
    if isinstance(other, NamedShape):
      return (self.__positional, self.__named) == (other.__positional, other.__named)
    if isinstance(other, tuple):
      return not self.__named and self.__positional == other
    return False

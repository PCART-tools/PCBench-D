  @property
  def total(self):
    total = 1
    for s in self.__positional: total *= s
    for s in self.__named.values(): total *= s
    return total

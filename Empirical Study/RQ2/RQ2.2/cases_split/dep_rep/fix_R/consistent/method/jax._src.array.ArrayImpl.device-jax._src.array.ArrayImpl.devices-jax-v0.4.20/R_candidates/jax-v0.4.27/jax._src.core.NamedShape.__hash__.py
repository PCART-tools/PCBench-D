  def __hash__(self):
    named = frozenset(self.__named.items())
    return hash((self.__positional, named))

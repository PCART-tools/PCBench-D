  def __str__(self):
    # TODO(mattjj,frostig): revise not to miss commas
    if not self.__named:
      return str(self.__positional)
    return (f"({', '.join(map(str, self.__positional))}{', ' if self.__named else ''}"
            f"{', '.join(f'{k}={v}' for k, v in self.__named.items())})")

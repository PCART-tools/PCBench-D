class FlagHolder(Generic[_T]):
  def __init__(self, name: str):
    self._name = name

  def __bool__(self) -> NoReturn:
    raise TypeError(
        "bool() not supported for instances of type '{0}' "
        "(did you mean to use '{0}.value' instead?)".format(
            type(self).__name__))

  @property
  def value(self) -> _T:
    return config.read(self._name)

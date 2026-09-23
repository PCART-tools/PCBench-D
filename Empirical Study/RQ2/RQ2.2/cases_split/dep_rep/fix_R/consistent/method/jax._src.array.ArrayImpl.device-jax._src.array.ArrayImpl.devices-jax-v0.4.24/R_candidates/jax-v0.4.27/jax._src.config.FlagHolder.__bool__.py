  def __bool__(self) -> NoReturn:
    raise TypeError(
        "bool() not supported for instances of type '{0}' "
        "(did you mean to use '{0}.value' instead?)".format(
            type(self).__name__))

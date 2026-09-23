    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except Exception:  # pragma: no cover
            self.__doc__ = ""
        self.name = wrapped.__name__

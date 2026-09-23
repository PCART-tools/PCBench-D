    def __init__(self, ufunc):
        if not isinstance(ufunc, np.ufunc):
            raise TypeError("must be an instance of `ufunc`, "
                            "got `%s" % type(ufunc).__name__)
        self._ufunc = ufunc
        self.__name__ = ufunc.__name__
        copy_docstring(self, ufunc)

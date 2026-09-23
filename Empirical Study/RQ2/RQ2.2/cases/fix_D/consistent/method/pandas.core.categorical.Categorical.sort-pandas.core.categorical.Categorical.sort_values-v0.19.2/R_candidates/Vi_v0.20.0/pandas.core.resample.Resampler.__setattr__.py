    def __setattr__(self, attr, value):
        if attr not in self._deprecated_valids:
            raise ValueError("cannot set values on {0}".format(
                self.__class__.__name__))
        object.__setattr__(self, attr, value)

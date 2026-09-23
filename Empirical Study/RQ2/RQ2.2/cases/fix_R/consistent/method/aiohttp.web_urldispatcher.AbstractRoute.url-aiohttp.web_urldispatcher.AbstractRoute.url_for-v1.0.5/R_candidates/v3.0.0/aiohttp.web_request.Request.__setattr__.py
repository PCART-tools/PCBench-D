    def __setattr__(self, name, val):
        if name not in self.ATTRS:
            warnings.warn("Setting custom {}.{} attribute "
                          "is discouraged".format(self.__class__.__name__,
                                                  name),
                          DeprecationWarning,
                          stacklevel=2)
        super().__setattr__(name, val)

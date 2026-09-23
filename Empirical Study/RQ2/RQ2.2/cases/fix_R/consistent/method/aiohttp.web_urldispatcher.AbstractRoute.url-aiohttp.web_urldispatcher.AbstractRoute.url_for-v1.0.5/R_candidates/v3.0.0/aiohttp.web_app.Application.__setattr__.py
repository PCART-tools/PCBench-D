    def __setattr__(self, name, val):
        if name not in self.ATTRS:
            warnings.warn("Setting custom web.Application.{} attribute "
                          "is discouraged".format(name),
                          DeprecationWarning,
                          stacklevel=2)
        super().__setattr__(name, val)

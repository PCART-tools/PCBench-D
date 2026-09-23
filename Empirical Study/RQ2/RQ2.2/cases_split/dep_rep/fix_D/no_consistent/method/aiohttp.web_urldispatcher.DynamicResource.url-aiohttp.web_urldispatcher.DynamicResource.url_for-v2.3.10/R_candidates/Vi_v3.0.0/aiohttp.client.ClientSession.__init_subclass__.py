    def __init_subclass__(cls):
        warnings.warn("Inheritance class {} from ClientSession "
                      "is discouraged".format(cls.__name__),
                      DeprecationWarning,
                      stacklevel=2)

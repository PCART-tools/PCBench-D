    def __init_subclass__(cls):
        warnings.warn("Inheritance class {} from web.Application "
                      "is discouraged".format(cls.__name__),
                      DeprecationWarning,
                      stacklevel=2)

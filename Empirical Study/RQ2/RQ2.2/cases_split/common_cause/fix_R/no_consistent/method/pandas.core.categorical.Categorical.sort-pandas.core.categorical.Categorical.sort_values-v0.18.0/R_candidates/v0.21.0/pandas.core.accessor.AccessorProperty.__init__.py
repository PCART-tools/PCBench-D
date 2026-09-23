    def __init__(self, accessor_cls, construct_accessor=None):
        self.accessor_cls = accessor_cls
        self.construct_accessor = (construct_accessor or
                                   accessor_cls._make_accessor)
        self.__doc__ = accessor_cls.__doc__

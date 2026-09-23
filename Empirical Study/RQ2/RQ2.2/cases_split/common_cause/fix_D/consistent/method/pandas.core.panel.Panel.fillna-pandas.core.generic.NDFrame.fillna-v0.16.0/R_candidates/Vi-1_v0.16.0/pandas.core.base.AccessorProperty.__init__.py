    def __init__(self, accessor_cls, construct_accessor):
        self.accessor_cls = accessor_cls
        self.construct_accessor = construct_accessor
        self.__doc__ = accessor_cls.__doc__

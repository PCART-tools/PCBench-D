    def __new__(cls, *args, **kwargs):
        return tuple.__new__(cls, args[0])

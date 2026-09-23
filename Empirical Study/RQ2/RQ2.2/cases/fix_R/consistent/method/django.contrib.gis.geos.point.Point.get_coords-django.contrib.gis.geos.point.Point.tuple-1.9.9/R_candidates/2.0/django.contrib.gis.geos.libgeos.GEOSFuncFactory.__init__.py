    def __init__(self, func_name, *args, restype=None, errcheck=None, argtypes=None, **kwargs):
        self.func_name = func_name
        if restype is not None:
            self.restype = restype
        if errcheck is not None:
            self.errcheck = errcheck
        if argtypes is not None:
            self.argtypes = argtypes
        self.args = args
        self.kwargs = kwargs

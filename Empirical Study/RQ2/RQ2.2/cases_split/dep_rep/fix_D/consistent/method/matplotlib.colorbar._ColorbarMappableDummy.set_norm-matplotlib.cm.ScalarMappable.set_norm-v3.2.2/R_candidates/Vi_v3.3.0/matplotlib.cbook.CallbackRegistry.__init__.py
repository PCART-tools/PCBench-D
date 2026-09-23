    def __init__(self, exception_handler=_exception_printer):
        self.exception_handler = exception_handler
        self.callbacks = {}
        self._cid_gen = itertools.count()
        self._func_cid_map = {}

    def __init__(self, exception_handler=_exception_printer):
        self.exception_handler = exception_handler
        self.callbacks = dict()
        self._cid = 0
        self._func_cid_map = {}

    def __init__(self, exception_handler=_exception_printer, *, signals=None):
        self._signals = None if signals is None else list(signals)  # Copy it.
        self.exception_handler = exception_handler
        self.callbacks = {}
        self._cid_gen = itertools.count()
        self._func_cid_map = _UnhashDict([])
        # A hidden variable that marks cids that need to be pickled.
        self._pickled_cids = set()

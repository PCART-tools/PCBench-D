    def __init__(self, http_exception):
        super().__init__(hdrs.METH_ANY, self._handler)
        self._http_exception = http_exception

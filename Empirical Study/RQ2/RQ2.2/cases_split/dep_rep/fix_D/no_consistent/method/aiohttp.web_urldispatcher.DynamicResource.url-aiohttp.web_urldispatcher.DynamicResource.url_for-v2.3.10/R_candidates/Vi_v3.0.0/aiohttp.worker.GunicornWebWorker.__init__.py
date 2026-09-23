    def __init__(self, *args, **kw):  # pragma: no cover
        super().__init__(*args, **kw)

        self._runner = None
        self._task = None
        self.exit_code = 0
        self._notify_waiter = None

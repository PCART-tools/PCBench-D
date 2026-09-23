    def __init__(self, app, *, handle_signals=False, **kwargs):
        super().__init__(handle_signals=handle_signals, **kwargs)
        self._app = app

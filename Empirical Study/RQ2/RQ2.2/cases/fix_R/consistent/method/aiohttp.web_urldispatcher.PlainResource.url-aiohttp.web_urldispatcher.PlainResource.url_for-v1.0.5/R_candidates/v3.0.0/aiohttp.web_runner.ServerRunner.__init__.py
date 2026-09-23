    def __init__(self, web_server, *, handle_signals=False, **kwargs):
        super().__init__(handle_signals=handle_signals, **kwargs)
        self._web_server = web_server

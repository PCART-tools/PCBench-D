    def __init__(self, *, handle_signals=False, **kwargs):
        self._handle_signals = handle_signals
        self._kwargs = kwargs
        self._server = None
        self._sites = set()

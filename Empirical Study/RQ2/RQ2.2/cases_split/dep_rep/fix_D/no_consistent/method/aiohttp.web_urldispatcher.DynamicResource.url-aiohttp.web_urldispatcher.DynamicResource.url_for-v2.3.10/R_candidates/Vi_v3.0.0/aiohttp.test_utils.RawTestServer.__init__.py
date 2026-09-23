    def __init__(self, handler, *,
                 scheme=sentinel, host='127.0.0.1', port=None, **kwargs):
        self._handler = handler
        super().__init__(scheme=scheme, host=host, port=port, **kwargs)

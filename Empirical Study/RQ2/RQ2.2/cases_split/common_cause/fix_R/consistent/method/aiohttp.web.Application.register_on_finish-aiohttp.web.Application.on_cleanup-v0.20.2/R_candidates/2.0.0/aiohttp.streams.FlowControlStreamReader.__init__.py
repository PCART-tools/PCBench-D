    def __init__(self, protocol, buffer_limit=DEFAULT_LIMIT, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._protocol = protocol
        self._b_limit = buffer_limit * 2

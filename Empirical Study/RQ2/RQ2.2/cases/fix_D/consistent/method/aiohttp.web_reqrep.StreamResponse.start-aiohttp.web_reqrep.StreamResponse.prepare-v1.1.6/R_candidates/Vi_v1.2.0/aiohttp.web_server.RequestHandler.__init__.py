    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self._manager = manager
        self._request_factory = manager.request_factory
        self._handler = manager.handler
        self.time_service = manager.time_service

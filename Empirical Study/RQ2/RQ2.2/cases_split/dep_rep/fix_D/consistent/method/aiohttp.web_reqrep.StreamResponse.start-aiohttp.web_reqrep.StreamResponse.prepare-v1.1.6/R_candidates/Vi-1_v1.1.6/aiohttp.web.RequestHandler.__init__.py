    def __init__(self, manager, app, router, time_service, *,
                 secure_proxy_ssl_header=None, **kwargs):
        super().__init__(**kwargs)

        self._manager = manager
        self._app = app
        self._router = router
        self._secure_proxy_ssl_header = secure_proxy_ssl_header
        self._time_service = time_service

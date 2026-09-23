    def __init__(self, *, logger=web_logger, router=None, middlewares=(),
                 handler_args=None, client_max_size=1024**2,
                 loop=None, debug=...):
        if router is None:
            router = web_urldispatcher.UrlDispatcher()
        assert isinstance(router, AbstractRouter), router

        if loop is not None:
            warnings.warn("loop argument is deprecated", ResourceWarning)

        self._debug = debug
        self._router = router
        self._secure_proxy_ssl_header = None
        self._loop = loop
        self._handler_args = handler_args
        self.logger = logger

        self._middlewares = FrozenList(middlewares)
        self._state = {}
        self._frozen = False
        self._subapps = []

        self._on_pre_signal = PreSignal()
        self._on_post_signal = PostSignal()
        self._on_loop_available = Signal(self)
        self._on_response_prepare = Signal(self)
        self._on_startup = Signal(self)
        self._on_shutdown = Signal(self)
        self._on_cleanup = Signal(self)
        self._client_max_size = client_max_size

    def __init__(self, *, logger=web_logger, loop=None,
                 router=None, handler_factory=RequestHandlerFactory,
                 middlewares=(), debug=False):
        if loop is None:
            loop = asyncio.get_event_loop()
        if router is None:
            router = web_urldispatcher.UrlDispatcher(self)
        assert isinstance(router, AbstractRouter), router

        self._debug = debug
        self._router = router
        self._handler_factory = handler_factory
        self._loop = loop
        self.logger = logger

        self._middlewares = FrozenList(middlewares)
        self._state = {}
        self._frozen = False

        self._on_pre_signal = PreSignal()
        self._on_post_signal = PostSignal()
        self._on_response_prepare = Signal(self)
        self._on_startup = Signal(self)
        self._on_shutdown = Signal(self)
        self._on_cleanup = Signal(self)

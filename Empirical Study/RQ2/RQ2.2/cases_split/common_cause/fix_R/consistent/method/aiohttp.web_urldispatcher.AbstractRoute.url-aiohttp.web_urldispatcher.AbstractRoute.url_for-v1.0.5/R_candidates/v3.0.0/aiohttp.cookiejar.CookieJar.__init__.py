    def __init__(self, *, unsafe=False, loop=None):
        super().__init__(loop=loop)
        self._cookies = defaultdict(SimpleCookie)
        self._host_only_cookies = set()
        self._unsafe = unsafe
        self._next_expiration = ceil(self._loop.time())
        self._expirations = {}

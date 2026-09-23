    def __init__(self, method, url, *,
                 writer=None, continue100=None, timer=None):
        assert isinstance(url, URL)

        self.method = method
        self.headers = None
        self.cookies = SimpleCookie()

        self._url = url
        self._content = None
        self._writer = writer
        self._continue = continue100
        self._closed = True
        self._history = ()
        self._timer = timer if timer is not None else TimerNoop()

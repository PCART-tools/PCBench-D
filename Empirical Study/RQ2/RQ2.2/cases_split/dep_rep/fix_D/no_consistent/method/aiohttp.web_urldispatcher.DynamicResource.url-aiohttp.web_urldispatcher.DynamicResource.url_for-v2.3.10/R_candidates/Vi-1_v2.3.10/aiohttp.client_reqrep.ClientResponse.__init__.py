    def __init__(self, method, url, *,
                 writer=None, continue100=None, timer=None,
                 request_info=None, auto_decompress=True):
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
        self._request_info = request_info
        self._timer = timer if timer is not None else TimerNoop()
        self._auto_decompress = auto_decompress

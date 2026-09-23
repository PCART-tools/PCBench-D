    def __init__(self, method, url, *, writer=None, continue100=None,
                 timeout=5*60):
        assert isinstance(url, URL)

        self.method = method
        self._url_obj = url
        self._content = None
        self._writer = writer
        self._continue = continue100
        self._closed = False
        self._should_close = True  # override by message.should_close later
        self._history = ()
        self._timeout = timeout
        self.cookies = http.cookies.SimpleCookie()

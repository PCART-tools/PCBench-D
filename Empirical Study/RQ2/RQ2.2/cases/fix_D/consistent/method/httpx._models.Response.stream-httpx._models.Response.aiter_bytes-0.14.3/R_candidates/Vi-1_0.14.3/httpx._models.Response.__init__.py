    def __init__(
        self,
        status_code: int,
        *,
        request: Request = None,
        http_version: str = None,
        headers: HeaderTypes = None,
        stream: ContentStream = None,
        content: bytes = None,
        history: typing.List["Response"] = None,
    ):
        self.status_code = status_code
        self.http_version = http_version
        self.headers = Headers(headers)

        self._request: typing.Optional[Request] = request

        self.call_next: typing.Optional[typing.Callable] = None

        self.history = [] if history is None else list(history)

        self.is_closed = False
        self.is_stream_consumed = False
        if stream is not None:
            self._raw_stream = stream
        else:
            self._raw_stream = ByteStream(body=content or b"")
            self.read()

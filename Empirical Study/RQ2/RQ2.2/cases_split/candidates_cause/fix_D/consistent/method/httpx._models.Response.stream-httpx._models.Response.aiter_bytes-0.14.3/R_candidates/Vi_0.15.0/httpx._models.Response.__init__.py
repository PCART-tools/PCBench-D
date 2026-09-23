    def __init__(
        self,
        status_code: int,
        *,
        headers: HeaderTypes = None,
        content: ResponseContent = None,
        text: str = None,
        html: str = None,
        json: typing.Any = None,
        stream: ByteStream = None,
        request: Request = None,
        ext: dict = None,
        history: typing.List["Response"] = None,
        on_close: typing.Callable = None,
    ):
        self.status_code = status_code
        self.headers = Headers(headers)

        self._request: typing.Optional[Request] = request

        self.call_next: typing.Optional[typing.Callable] = None

        self.ext = {} if ext is None else ext
        self.history = [] if history is None else list(history)
        self._on_close = on_close

        self.is_closed = False
        self.is_stream_consumed = False

        if stream is not None:
            # There's an important distinction between `Response(content=...)`,
            # and `Response(stream=...)`.
            #
            # Using `content=...` implies automatically populated content headers,
            # of either `Content-Length: ...` or `Transfer-Encoding: chunked`.
            #
            # Using `stream=...` will not automatically include any content headers.
            #
            # As an end-user you don't really need `stream=...`. It's only
            # useful when creating response instances having received a stream
            # from the transport API.
            self.stream = stream
        else:
            headers, stream = encode_response(content, text, html, json)
            self._prepare(headers)
            self.stream = stream
            if content is None or isinstance(content, bytes):
                # Load the response body, except for streaming content.
                self.read()

        self._num_bytes_downloaded = 0

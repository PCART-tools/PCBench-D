class Request:
    def __init__(
        self,
        method: typing.Union[str, bytes],
        url: typing.Union["URL", str, RawURL],
        *,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        content: RequestContent = None,
        data: RequestData = None,
        files: RequestFiles = None,
        json: typing.Any = None,
        stream: ByteStream = None,
    ):
        if isinstance(method, bytes):
            self.method = method.decode("ascii").upper()
        else:
            self.method = method.upper()
        self.url = URL(url, params=params)
        self.headers = Headers(headers)
        if cookies:
            Cookies(cookies).set_cookie_header(self)

        if stream is not None:
            # There's an important distinction between `Request(content=...)`,
            # and `Request(stream=...)`.
            #
            # Using `content=...` implies automatically populated content headers,
            # of either `Content-Length: ...` or `Transfer-Encoding: chunked`.
            #
            # Using `stream=...` will not automatically include any content headers.
            #
            # As an end-user you don't really need `stream=...`. It's only
            # useful when:
            #
            # * Preserving the request stream when copying requests, eg for redirects.
            # * Creating request instances on the *server-side* of the transport API.
            self.stream = stream
            self._prepare({})
        else:
            headers, stream = encode_request(content, data, files, json)
            self._prepare(headers)
            self.stream = stream

    def _prepare(self, default_headers: typing.Dict[str, str]) -> None:
        for key, value in default_headers.items():
            # Ignore Transfer-Encoding if the Content-Length has been set explicitly.
            if key.lower() == "transfer-encoding" and "content-length" in self.headers:
                continue
            self.headers.setdefault(key, value)

        auto_headers: typing.List[typing.Tuple[bytes, bytes]] = []

        has_host = "host" in self.headers
        has_content_length = (
            "content-length" in self.headers or "transfer-encoding" in self.headers
        )

        if not has_host and self.url.host:
            default_port = {"http": 80, "https": 443}.get(self.url.scheme)
            if self.url.port is None or self.url.port == default_port:
                host_header = self.url.host.encode("ascii")
            else:
                host_header = self.url.netloc.encode("ascii")
            auto_headers.append((b"host", host_header))
        if not has_content_length and self.method in ("POST", "PUT", "PATCH"):
            auto_headers.append((b"content-length", b"0"))

        self.headers = Headers(auto_headers + self.headers.raw)

    @property
    def content(self) -> bytes:
        if not hasattr(self, "_content"):
            raise RequestNotRead()
        return self._content

    def read(self) -> bytes:
        """
        Read and return the request content.
        """
        if not hasattr(self, "_content"):
            assert isinstance(self.stream, typing.Iterable)
            self._content = b"".join(self.stream)
            # If a streaming request has been read entirely into memory, then
            # we can replace the stream with a raw bytes implementation,
            # to ensure that any non-replayable streams can still be used.
            self.stream = PlainByteStream(self._content)
        return self._content

    async def aread(self) -> bytes:
        """
        Read and return the request content.
        """
        if not hasattr(self, "_content"):
            assert isinstance(self.stream, typing.AsyncIterable)
            self._content = b"".join([part async for part in self.stream])
            # If a streaming request has been read entirely into memory, then
            # we can replace the stream with a raw bytes implementation,
            # to ensure that any non-replayable streams can still be used.
            self.stream = PlainByteStream(self._content)
        return self._content

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        url = str(self.url)
        return f"<{class_name}({self.method!r}, {url!r})>"

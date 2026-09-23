class Response:
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

    def _prepare(self, default_headers: typing.Dict[str, str]) -> None:
        for key, value in default_headers.items():
            # Ignore Transfer-Encoding if the Content-Length has been set explicitly.
            if key.lower() == "transfer-encoding" and "content-length" in self.headers:
                continue
            self.headers.setdefault(key, value)

    @property
    def elapsed(self) -> datetime.timedelta:
        """
        Returns the time taken for the complete request/response
        cycle to complete.
        """
        if not hasattr(self, "_elapsed"):
            raise RuntimeError(
                "'.elapsed' may only be accessed after the response "
                "has been read or closed."
            )
        return self._elapsed

    @elapsed.setter
    def elapsed(self, elapsed: datetime.timedelta) -> None:
        self._elapsed = elapsed

    @property
    def request(self) -> Request:
        """
        Returns the request instance associated to the current response.
        """
        if self._request is None:
            raise RuntimeError(
                "The request instance has not been set on this response."
            )
        return self._request

    @request.setter
    def request(self, value: Request) -> None:
        self._request = value

    @property
    def http_version(self) -> str:
        return self.ext.get("http_version", "HTTP/1.1")

    @property
    def reason_phrase(self) -> str:
        return self.ext.get("reason", codes.get_reason_phrase(self.status_code))

    @property
    def url(self) -> typing.Optional[URL]:
        """
        Returns the URL for which the request was made.
        """
        return self.request.url

    @property
    def content(self) -> bytes:
        if not hasattr(self, "_content"):
            raise ResponseNotRead()
        return self._content

    @property
    def text(self) -> str:
        if not hasattr(self, "_text"):
            content = self.content
            if not content:
                self._text = ""
            else:
                decoder = TextDecoder(encoding=self.encoding)
                self._text = "".join([decoder.decode(self.content), decoder.flush()])
        return self._text

    @property
    def encoding(self) -> typing.Optional[str]:
        """
        Return the encoding, which may have been set explicitly, or may have
        been specified by the Content-Type header.
        """
        if not hasattr(self, "_encoding"):
            encoding = self.charset_encoding
            if encoding is None or not is_known_encoding(encoding):
                self._encoding = None
            else:
                self._encoding = encoding
        return self._encoding

    @encoding.setter
    def encoding(self, value: str) -> None:
        self._encoding = value

    @property
    def charset_encoding(self) -> typing.Optional[str]:
        """
        Return the encoding, as specified by the Content-Type header.
        """
        content_type = self.headers.get("Content-Type")
        if content_type is None:
            return None

        _, params = cgi.parse_header(content_type)
        if "charset" not in params:
            return None

        return params["charset"].strip("'\"")

    def _get_content_decoder(self) -> ContentDecoder:
        """
        Returns a decoder instance which can be used to decode the raw byte
        content, depending on the Content-Encoding used in the response.
        """
        if not hasattr(self, "_decoder"):
            decoders: typing.List[ContentDecoder] = []
            values = self.headers.get_list("content-encoding", split_commas=True)
            for value in values:
                value = value.strip().lower()
                try:
                    decoder_cls = SUPPORTED_DECODERS[value]
                    decoders.append(decoder_cls())
                except KeyError:
                    continue

            if len(decoders) == 1:
                self._decoder = decoders[0]
            elif len(decoders) > 1:
                self._decoder = MultiDecoder(children=decoders)
            else:
                self._decoder = IdentityDecoder()

        return self._decoder

    @property
    def is_error(self) -> bool:
        return codes.is_error(self.status_code)

    @property
    def is_redirect(self) -> bool:
        return codes.is_redirect(self.status_code) and "location" in self.headers

    def raise_for_status(self) -> None:
        """
        Raise the `HTTPStatusError` if one occurred.
        """
        message = (
            "{0.status_code} {error_type}: {0.reason_phrase} for url: {0.url}\n"
            "For more information check: https://httpstatuses.com/{0.status_code}"
        )

        request = self._request
        if request is None:
            raise RuntimeError(
                "Cannot call `raise_for_status` as the request "
                "instance has not been set on this response."
            )

        if codes.is_client_error(self.status_code):
            message = message.format(self, error_type="Client Error")
            raise HTTPStatusError(message, request=request, response=self)
        elif codes.is_server_error(self.status_code):
            message = message.format(self, error_type="Server Error")
            raise HTTPStatusError(message, request=request, response=self)

    def json(self, **kwargs: typing.Any) -> typing.Any:
        if self.charset_encoding is None and self.content and len(self.content) > 3:
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                try:
                    return jsonlib.loads(self.content.decode(encoding), **kwargs)
                except UnicodeDecodeError:
                    pass
        return jsonlib.loads(self.text, **kwargs)

    @property
    def cookies(self) -> "Cookies":
        if not hasattr(self, "_cookies"):
            self._cookies = Cookies()
            self._cookies.extract_cookies(self)
        return self._cookies

    @property
    def links(self) -> typing.Dict[typing.Optional[str], typing.Dict[str, str]]:
        """
        Returns the parsed header links of the response, if any
        """
        header = self.headers.get("link")
        ldict = {}
        if header:
            links = parse_header_links(header)
            for link in links:
                key = link.get("rel") or link.get("url")
                ldict[key] = link
        return ldict

    @property
    def num_bytes_downloaded(self) -> int:
        return self._num_bytes_downloaded

    def __repr__(self) -> str:
        return f"<Response [{self.status_code} {self.reason_phrase}]>"

    @contextlib.contextmanager
    def _wrap_decoder_errors(self) -> typing.Iterator[None]:
        # If the response has an associated request instance, we want decoding
        # errors to be raised as proper `httpx.DecodingError` exceptions.
        try:
            yield
        except ValueError as exc:
            if self._request is None:
                raise exc
            raise DecodingError(message=str(exc), request=self.request) from exc

    def read(self) -> bytes:
        """
        Read and return the response content.
        """
        if not hasattr(self, "_content"):
            self._content = b"".join(self.iter_bytes())
        return self._content

    def iter_bytes(self) -> typing.Iterator[bytes]:
        """
        A byte-iterator over the decoded response content.
        This allows us to handle gzip, deflate, and brotli encoded responses.
        """
        if hasattr(self, "_content"):
            yield self._content
        else:
            decoder = self._get_content_decoder()
            with self._wrap_decoder_errors():
                for chunk in self.iter_raw():
                    yield decoder.decode(chunk)
                yield decoder.flush()

    def iter_text(self) -> typing.Iterator[str]:
        """
        A str-iterator over the decoded response content
        that handles both gzip, deflate, etc but also detects the content's
        string encoding.
        """
        decoder = TextDecoder(encoding=self.encoding)
        with self._wrap_decoder_errors():
            for chunk in self.iter_bytes():
                yield decoder.decode(chunk)
            yield decoder.flush()

    def iter_lines(self) -> typing.Iterator[str]:
        decoder = LineDecoder()
        with self._wrap_decoder_errors():
            for text in self.iter_text():
                for line in decoder.decode(text):
                    yield line
            for line in decoder.flush():
                yield line

    def iter_raw(self) -> typing.Iterator[bytes]:
        """
        A byte-iterator over the raw response content.
        """
        if self.is_stream_consumed:
            raise StreamConsumed()
        if self.is_closed:
            raise ResponseClosed()
        if not isinstance(self.stream, typing.Iterable):
            raise RuntimeError("Attempted to call a sync iterator on an async stream.")

        self.is_stream_consumed = True
        self._num_bytes_downloaded = 0
        with map_exceptions(HTTPCORE_EXC_MAP, request=self._request):
            for part in self.stream:
                self._num_bytes_downloaded += len(part)
                yield part
        self.close()

    def next(self) -> "Response":
        """
        Get the next response from a redirect response.
        """
        if not self.is_redirect:
            message = (
                "Called .next(), but the response was not a redirect. "
                "Calling code should check `response.is_redirect` first."
            )
            raise NotRedirectResponse(message)
        assert self.call_next is not None
        return self.call_next()

    def close(self) -> None:
        """
        Close the response and release the connection.
        Automatically called if the response body is read to completion.
        """
        if not self.is_closed:
            self.is_closed = True
            if self._on_close is not None:
                self._on_close(self)

    async def aread(self) -> bytes:
        """
        Read and return the response content.
        """
        if not hasattr(self, "_content"):
            self._content = b"".join([part async for part in self.aiter_bytes()])
        return self._content

    async def aiter_bytes(self) -> typing.AsyncIterator[bytes]:
        """
        A byte-iterator over the decoded response content.
        This allows us to handle gzip, deflate, and brotli encoded responses.
        """
        if hasattr(self, "_content"):
            yield self._content
        else:
            decoder = self._get_content_decoder()
            with self._wrap_decoder_errors():
                async for chunk in self.aiter_raw():
                    yield decoder.decode(chunk)
                yield decoder.flush()

    async def aiter_text(self) -> typing.AsyncIterator[str]:
        """
        A str-iterator over the decoded response content
        that handles both gzip, deflate, etc but also detects the content's
        string encoding.
        """
        decoder = TextDecoder(encoding=self.encoding)
        with self._wrap_decoder_errors():
            async for chunk in self.aiter_bytes():
                yield decoder.decode(chunk)
            yield decoder.flush()

    async def aiter_lines(self) -> typing.AsyncIterator[str]:
        decoder = LineDecoder()
        with self._wrap_decoder_errors():
            async for text in self.aiter_text():
                for line in decoder.decode(text):
                    yield line
            for line in decoder.flush():
                yield line

    async def aiter_raw(self) -> typing.AsyncIterator[bytes]:
        """
        A byte-iterator over the raw response content.
        """
        if self.is_stream_consumed:
            raise StreamConsumed()
        if self.is_closed:
            raise ResponseClosed()
        if not isinstance(self.stream, typing.AsyncIterable):
            raise RuntimeError("Attempted to call a async iterator on a sync stream.")

        self.is_stream_consumed = True
        self._num_bytes_downloaded = 0
        with map_exceptions(HTTPCORE_EXC_MAP, request=self._request):
            async for part in self.stream:
                self._num_bytes_downloaded += len(part)
                yield part
        await self.aclose()

    async def anext(self) -> "Response":
        """
        Get the next response from a redirect response.
        """
        if not self.is_redirect:
            raise NotRedirectResponse(
                "Called .anext(), but the response was not a redirect. "
                "Calling code should check `response.is_redirect` first."
            )
        assert self.call_next is not None
        return await self.call_next()

    async def aclose(self) -> None:
        """
        Close the response and release the connection.
        Automatically called if the response body is read to completion.
        """
        if not self.is_closed:
            self.is_closed = True
            if self._on_close is not None:
                await self._on_close(self)

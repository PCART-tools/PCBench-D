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

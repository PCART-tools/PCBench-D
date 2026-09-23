    def __init__(
        self,
        method: str,
        url: typing.Union[str, URL],
        *,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        data: RequestData = None,
        files: RequestFiles = None,
        json: typing.Any = None,
        stream: ContentStream = None,
    ):
        self.method = method.upper()
        self.url = URL(url, params=params)
        self.headers = Headers(headers)
        if cookies:
            Cookies(cookies).set_cookie_header(self)

        if stream is not None:
            self.stream = stream
        else:
            self.stream = encode(data, files, json)

        self.timer = ElapsedTimer()
        self.prepare()

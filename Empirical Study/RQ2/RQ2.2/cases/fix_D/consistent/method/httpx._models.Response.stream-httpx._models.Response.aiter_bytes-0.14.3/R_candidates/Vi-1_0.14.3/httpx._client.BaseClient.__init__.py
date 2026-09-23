    def __init__(
        self,
        *,
        auth: AuthTypes = None,
        params: QueryParamTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        base_url: URLTypes = "",
        trust_env: bool = True,
    ):
        self._base_url = self._enforce_trailing_slash(URL(base_url))

        self._auth = self._build_auth(auth)
        self._params = QueryParams(params)
        self._headers = Headers(headers)
        self._cookies = Cookies(cookies)
        self._timeout = Timeout(timeout)
        self.max_redirects = max_redirects
        self._trust_env = trust_env
        self._netrc = NetRCInfo()

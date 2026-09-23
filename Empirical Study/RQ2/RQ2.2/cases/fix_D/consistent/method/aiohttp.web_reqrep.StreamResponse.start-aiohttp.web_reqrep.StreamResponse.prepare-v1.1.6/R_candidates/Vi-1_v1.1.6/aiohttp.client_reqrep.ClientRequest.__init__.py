    def __init__(self, method, url, *,
                 params=None, headers=None, skip_auto_headers=frozenset(),
                 data=None, cookies=None,
                 auth=None, encoding='utf-8',
                 version=aiohttp.HttpVersion11, compress=None,
                 chunked=None, expect100=False,
                 loop=None, response_class=None,
                 proxy=None, proxy_auth=None,
                 timeout=5*60):

        if loop is None:
            loop = asyncio.get_event_loop()

        assert isinstance(url, URL), url
        assert isinstance(proxy, (URL, type(None))), proxy

        if params:
            q = MultiDict(url.query)
            url2 = url.with_query(params)
            q.extend(url2.query)
            url = url.with_query(q)
        self.url = url.with_fragment(None)
        self.method = method.upper()
        self.encoding = encoding
        self.chunked = chunked
        self.compress = compress
        self.loop = loop
        self.response_class = response_class or ClientResponse
        self._timeout = timeout

        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

        self.update_version(version)
        self.update_host(url)
        self.update_headers(headers)
        self.update_auto_headers(skip_auto_headers)
        self.update_cookies(cookies)
        self.update_content_encoding(data)
        self.update_auth(auth)
        self.update_proxy(proxy, proxy_auth)

        self.update_body_from_data(data, skip_auto_headers)
        self.update_transfer_encoding()
        self.update_expect_continue(expect100)

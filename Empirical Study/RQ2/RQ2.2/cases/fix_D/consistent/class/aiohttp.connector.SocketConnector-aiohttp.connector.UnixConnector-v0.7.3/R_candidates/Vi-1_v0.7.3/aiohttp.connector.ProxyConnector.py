class ProxyConnector(TCPConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxies = kwargs['proxies']
        if 'https' in self.proxies:
            raise NotImplementedError(
                'Only http connections are supported via proxy now.')

    @asyncio.coroutine
    def connect(self, req):
        # substite request for proxy request to make initial connection
        proxy_req = aiohttp.client.HttpRequest(
            method='GET',
            url=self.proxies[req.scheme],
        )
        proxy_conn = yield from super().connect(proxy_req)
        proxy_conn._request = req  # putting original request back
        return proxy_conn

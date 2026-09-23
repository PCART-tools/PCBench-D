    def __init__(self, proxy, *, proxy_auth=None, force_close=True,
                 conn_timeout=None, keepalive_timeout=sentinel,
                 limit=20, loop=None):
        warnings.warn("ProxyConnector is deprecated, use "
                      "client.get(url, proxy=proxy_url) instead",
                      DeprecationWarning)
        super().__init__(force_close=force_close,
                         conn_timeout=conn_timeout,
                         keepalive_timeout=keepalive_timeout,
                         limit=limit, loop=loop)
        proxy = URL(proxy)
        self._proxy = proxy
        self._proxy_auth = proxy_auth

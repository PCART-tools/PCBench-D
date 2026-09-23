    def update_proxy(self, proxy, proxy_auth, proxy_headers):
        if proxy and not proxy.scheme == 'http':
            raise ValueError("Only http proxies are supported")
        if proxy_auth and not isinstance(proxy_auth, helpers.BasicAuth):
            raise ValueError("proxy_auth must be None or BasicAuth() tuple")
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.proxy_headers = proxy_headers

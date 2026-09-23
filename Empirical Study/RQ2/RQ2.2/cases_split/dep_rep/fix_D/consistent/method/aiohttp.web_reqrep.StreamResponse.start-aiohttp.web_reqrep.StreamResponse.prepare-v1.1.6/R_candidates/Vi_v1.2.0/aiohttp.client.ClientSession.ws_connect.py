    def ws_connect(self, url, *,
                   protocols=(),
                   timeout=10.0,
                   autoclose=True,
                   autoping=True,
                   auth=None,
                   origin=None,
                   headers=None,
                   proxy=None,
                   proxy_auth=None):
        """Initiate websocket connection."""
        return _WSRequestContextManager(
            self._ws_connect(url,
                             protocols=protocols,
                             timeout=timeout,
                             autoclose=autoclose,
                             autoping=autoping,
                             auth=auth,
                             origin=origin,
                             headers=headers,
                             proxy=proxy,
                             proxy_auth=proxy_auth))

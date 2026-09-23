    def _transport_for_url(self, url: URL) -> httpcore.AsyncHTTPTransport:
        """
        Returns the transport instance that should be used for a given URL.
        This will either be the standard connection pool, or a proxy.
        """
        for pattern, transport in self._proxies.items():
            if pattern.matches(url):
                return self._transport if transport is None else transport

        return self._transport

    def request(self, method, url, **kwargs):
        """Perform HTTP request."""
        return _RequestContextManager(self._request(method, url, **kwargs))

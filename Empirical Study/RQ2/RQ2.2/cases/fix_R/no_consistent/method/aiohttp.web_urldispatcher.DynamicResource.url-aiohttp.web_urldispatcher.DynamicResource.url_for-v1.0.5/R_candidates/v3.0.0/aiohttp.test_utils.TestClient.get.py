    def get(self, path, *args, **kwargs):
        """Perform an HTTP GET request."""
        return _RequestContextManager(
            self.request(hdrs.METH_GET, path, *args, **kwargs)
        )

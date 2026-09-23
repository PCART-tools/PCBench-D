    def put(self, path, *args, **kwargs):
        """Perform an HTTP PUT request."""
        return _RequestContextManager(
            self.request(hdrs.METH_PUT, path, *args, **kwargs)
        )

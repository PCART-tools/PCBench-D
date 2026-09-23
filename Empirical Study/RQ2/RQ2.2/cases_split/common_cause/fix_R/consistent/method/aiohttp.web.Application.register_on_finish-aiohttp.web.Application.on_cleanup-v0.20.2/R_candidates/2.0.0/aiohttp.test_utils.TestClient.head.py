    def head(self, path, *args, **kwargs):
        """Perform an HTTP HEAD request."""
        return _RequestContextManager(
            self.request(hdrs.METH_HEAD, path, *args, **kwargs)
        )

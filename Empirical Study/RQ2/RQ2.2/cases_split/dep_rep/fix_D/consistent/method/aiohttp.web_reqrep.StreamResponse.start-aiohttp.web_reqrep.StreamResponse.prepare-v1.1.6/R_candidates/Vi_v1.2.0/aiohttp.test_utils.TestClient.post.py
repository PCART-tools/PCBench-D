    def post(self, path, *args, **kwargs):
        """Perform an HTTP POST request."""
        return _RequestContextManager(
            self.request(hdrs.METH_POST, path, *args, **kwargs)
        )

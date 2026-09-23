    def options(self, path, *args, **kwargs):
        """Perform an HTTP OPTIONS request."""
        return _RequestContextManager(
            self.request(hdrs.METH_OPTIONS, path, *args, **kwargs)
        )

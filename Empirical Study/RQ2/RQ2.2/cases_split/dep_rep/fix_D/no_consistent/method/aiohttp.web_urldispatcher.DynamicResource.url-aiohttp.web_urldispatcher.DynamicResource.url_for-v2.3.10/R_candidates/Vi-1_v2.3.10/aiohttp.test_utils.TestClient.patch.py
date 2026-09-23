    def patch(self, path, *args, **kwargs):
        """Perform an HTTP PATCH request."""
        return _RequestContextManager(
            self.request(hdrs.METH_PATCH, path, *args, **kwargs)
        )

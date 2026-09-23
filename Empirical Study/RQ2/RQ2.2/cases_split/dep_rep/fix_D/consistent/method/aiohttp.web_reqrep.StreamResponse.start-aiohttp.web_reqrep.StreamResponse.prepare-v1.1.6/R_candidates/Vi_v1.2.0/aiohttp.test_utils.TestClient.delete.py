    def delete(self, path, *args, **kwargs):
        """Perform an HTTP PATCH request."""
        return _RequestContextManager(
            self.request(hdrs.METH_DELETE, path, *args, **kwargs)
        )

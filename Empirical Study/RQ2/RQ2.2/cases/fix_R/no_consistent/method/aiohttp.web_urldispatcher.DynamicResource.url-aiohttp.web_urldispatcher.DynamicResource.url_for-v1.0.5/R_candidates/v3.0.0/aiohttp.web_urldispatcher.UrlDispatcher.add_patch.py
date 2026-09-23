    def add_patch(self, path, handler, **kwargs):
        """
        Shortcut for add_route with method PATCH
        """
        return self.add_route(hdrs.METH_PATCH, path, handler, **kwargs)

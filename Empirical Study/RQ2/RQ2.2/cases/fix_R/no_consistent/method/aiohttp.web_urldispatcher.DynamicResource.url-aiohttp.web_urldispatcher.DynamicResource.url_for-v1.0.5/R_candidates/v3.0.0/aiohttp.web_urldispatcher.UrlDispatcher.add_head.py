    def add_head(self, path, handler, **kwargs):
        """
        Shortcut for add_route with method HEAD
        """
        return self.add_route(hdrs.METH_HEAD, path, handler, **kwargs)

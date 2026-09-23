    def add_put(self, path, handler, **kwargs):
        """
        Shortcut for add_route with method PUT
        """
        return self.add_route(hdrs.METH_PUT, path, handler, **kwargs)

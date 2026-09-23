    def add_post(self, path, handler, **kwargs):
        """
        Shortcut for add_route with method POST
        """
        return self.add_route(hdrs.METH_POST, path, handler, **kwargs)

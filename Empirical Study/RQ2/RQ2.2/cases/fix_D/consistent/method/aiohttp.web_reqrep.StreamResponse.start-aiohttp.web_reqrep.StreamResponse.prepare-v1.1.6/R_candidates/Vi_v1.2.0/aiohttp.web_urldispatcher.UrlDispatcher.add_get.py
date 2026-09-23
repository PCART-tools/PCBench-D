    def add_get(self, *args, **kwargs):
        """
        Shortcut for add_route with method GET
        """
        return self.add_route(hdrs.METH_GET, *args, **kwargs)

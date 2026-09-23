    def add_post(self, *args, **kwargs):
        """
        Shortcut for add_route with method POST
        """
        return self.add_route(hdrs.METH_POST, *args, **kwargs)

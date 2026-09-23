    def add_get(self, *args, name=None, allow_head=True, **kwargs):
        """
        Shortcut for add_route with method GET, if allow_head is true another
        route is added allowing head requests to the same endpoint
        """
        if allow_head:
            # the head route can't have "name" set or it would conflict with
            # the GET route below
            self.add_route(hdrs.METH_HEAD, *args, **kwargs)
        return self.add_route(hdrs.METH_GET, *args, name=name, **kwargs)

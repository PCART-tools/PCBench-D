    def add_get(self, path, handler, *, name=None, allow_head=True, **kwargs):
        """
        Shortcut for add_route with method GET, if allow_head is true another
        route is added allowing head requests to the same endpoint
        """
        if allow_head:
            # it name is not None append -head to avoid it conflicting with
            # the GET route below
            head_name = name and '{}-head'.format(name)
            self.add_route(hdrs.METH_HEAD, path, handler,
                           name=head_name, **kwargs)
        return self.add_route(hdrs.METH_GET, path, handler, name=name,
                              **kwargs)

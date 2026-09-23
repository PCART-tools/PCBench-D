    def add_delete(self, path, handler, **kwargs):
        """
        Shortcut for add_route with method DELETE
        """
        return self.add_route(hdrs.METH_DELETE, path, handler, **kwargs)

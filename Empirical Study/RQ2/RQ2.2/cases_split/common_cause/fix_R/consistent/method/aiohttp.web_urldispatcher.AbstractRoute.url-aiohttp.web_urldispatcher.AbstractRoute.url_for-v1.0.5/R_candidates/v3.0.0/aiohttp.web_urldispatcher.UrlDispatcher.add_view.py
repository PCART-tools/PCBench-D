    def add_view(self, path, handler, **kwargs):
        """
        Shortcut for add_route with ANY methods for a class-based view
        """
        return self.add_route(hdrs.METH_ANY, path, handler, **kwargs)

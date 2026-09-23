    def view(self, path, **kwargs):
        return self.route(hdrs.METH_ANY, path, **kwargs)

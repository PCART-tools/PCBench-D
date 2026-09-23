    def get(self, path, **kwargs):
        return self.route(hdrs.METH_GET, path, **kwargs)

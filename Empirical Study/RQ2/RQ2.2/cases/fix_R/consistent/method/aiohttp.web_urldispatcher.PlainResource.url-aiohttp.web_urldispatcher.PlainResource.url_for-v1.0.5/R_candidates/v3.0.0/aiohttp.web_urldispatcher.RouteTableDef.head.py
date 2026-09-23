    def head(self, path, **kwargs):
        return self.route(hdrs.METH_HEAD, path, **kwargs)

    def post(self, path, **kwargs):
        return self.route(hdrs.METH_POST, path, **kwargs)

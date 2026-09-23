    def patch(self, path, **kwargs):
        return self.route(hdrs.METH_PATCH, path, **kwargs)

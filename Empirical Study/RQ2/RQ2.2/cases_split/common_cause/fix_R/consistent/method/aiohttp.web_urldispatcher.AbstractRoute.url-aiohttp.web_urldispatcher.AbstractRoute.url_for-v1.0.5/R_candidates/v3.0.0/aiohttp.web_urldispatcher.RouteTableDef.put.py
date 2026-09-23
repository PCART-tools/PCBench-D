    def put(self, path, **kwargs):
        return self.route(hdrs.METH_PUT, path, **kwargs)

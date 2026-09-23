    def delete(self, path, **kwargs):
        return self.route(hdrs.METH_DELETE, path, **kwargs)

    def register(self, router):
        if self.method in hdrs.METH_ALL:
            reg = getattr(router, 'add_'+self.method.lower())
            reg(self.path, self.handler, **self.kwargs)
        else:
            router.add_route(self.method, self.path, self.handler,
                             **self.kwargs)

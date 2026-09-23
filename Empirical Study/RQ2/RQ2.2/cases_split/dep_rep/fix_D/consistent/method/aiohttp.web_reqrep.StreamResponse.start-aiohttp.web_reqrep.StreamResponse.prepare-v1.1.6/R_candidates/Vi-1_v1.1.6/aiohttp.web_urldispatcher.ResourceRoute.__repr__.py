    def __repr__(self):
        return "<ResourceRoute [{method}] {resource} -> {handler!r}".format(
            method=self.method, resource=self._resource,
            handler=self.handler)

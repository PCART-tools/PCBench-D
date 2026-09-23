    def route(self, method, path, **kwargs):
        def inner(handler):
            self._items.append(RouteDef(method, path, handler, kwargs))
            return handler
        return inner

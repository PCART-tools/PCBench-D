    def add_route(self, method, handler, *,
                  expect_handler=None):

        for route in self._routes:
            if route.method == method or route.method == hdrs.METH_ANY:
                raise RuntimeError("Added route will never be executed, "
                                   "method {route.method} is "
                                   "already registered".format(route=route))

        route = ResourceRoute(method, handler, self,
                              expect_handler=expect_handler)
        self.register_route(route)
        return route

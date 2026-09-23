    def add_route(self, method, handler, *,
                  expect_handler=None):

        for route_obj in self._routes:
            if route_obj.method == method or route_obj.method == hdrs.METH_ANY:
                raise RuntimeError("Added route will never be executed, "
                                   "method {route.method} is already "
                                   "registered".format(route=route_obj))

        route_obj = ResourceRoute(method, handler, self,
                                  expect_handler=expect_handler)
        self.register_route(route_obj)
        return route_obj

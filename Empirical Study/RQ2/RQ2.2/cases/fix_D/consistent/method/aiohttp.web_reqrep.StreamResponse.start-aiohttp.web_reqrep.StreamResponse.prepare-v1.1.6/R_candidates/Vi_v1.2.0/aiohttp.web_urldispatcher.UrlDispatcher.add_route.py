    def add_route(self, method, path, handler,
                  *, name=None, expect_handler=None):
        resource = self.add_resource(path, name=name)
        return resource.add_route(method, handler,
                                  expect_handler=expect_handler)

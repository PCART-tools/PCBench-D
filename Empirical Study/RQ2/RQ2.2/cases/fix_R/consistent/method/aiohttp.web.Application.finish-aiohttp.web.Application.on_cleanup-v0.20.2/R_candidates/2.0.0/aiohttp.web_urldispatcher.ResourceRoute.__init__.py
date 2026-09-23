    def __init__(self, method, handler, resource, *,
                 expect_handler=None):
        super().__init__(method, handler, expect_handler=expect_handler,
                         resource=resource)

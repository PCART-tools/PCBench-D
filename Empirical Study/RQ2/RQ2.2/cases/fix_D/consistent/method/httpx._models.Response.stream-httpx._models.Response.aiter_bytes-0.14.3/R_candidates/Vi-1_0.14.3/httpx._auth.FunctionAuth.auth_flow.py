    def auth_flow(self, request: Request) -> typing.Generator[Request, Response, None]:
        yield self._func(request)

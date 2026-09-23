    @asyncio.coroutine
    def resolve(self, request):
        if not request.url.raw_path.startswith(self._prefix):
            return None, set()
        match_info = yield from self._app.router.resolve(request)
        match_info.add_app(self._app)
        if isinstance(match_info.http_exception, HTTPMethodNotAllowed):
            methods = match_info.http_exception.allowed_methods
        else:
            methods = set()
        return (match_info, methods)

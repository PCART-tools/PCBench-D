    @asyncio.coroutine
    def prepare(self, request):
        resp_impl = self._start_pre_check(request)
        if resp_impl is not None:
            return resp_impl
        for app in request.match_info.apps:
            yield from app.on_response_prepare.send(request, self)

        return self._start(request)

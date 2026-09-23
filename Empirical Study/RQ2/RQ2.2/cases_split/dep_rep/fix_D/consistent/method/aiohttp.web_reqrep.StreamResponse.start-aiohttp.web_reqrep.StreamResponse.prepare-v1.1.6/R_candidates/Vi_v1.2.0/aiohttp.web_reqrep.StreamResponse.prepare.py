    @asyncio.coroutine
    def prepare(self, request):
        resp_impl = self._start_pre_check(request)
        if resp_impl is not None:
            return resp_impl
        yield from request._prepare_hook(self)

        return self._start(request)

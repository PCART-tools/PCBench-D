    @asyncio.coroutine
    def prepare(self, request):
        # make pre-check to don't hide it by do_handshake() exceptions
        resp_impl = self._start_pre_check(request)
        if resp_impl is not None:
            return resp_impl

        parser, protocol, writer = self._pre_start(request)
        resp_impl = yield from super().prepare(request)
        self._post_start(request, parser, protocol, writer)
        return resp_impl

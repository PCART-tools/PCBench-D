    @asyncio.coroutine
    def handle_expect_header(self, request):
        return (yield from self._expect_handler(request))

    @asyncio.coroutine
    def _send(self, *args, **kwargs):
        for receiver in self:
            res = receiver(*args, **kwargs)
            if asyncio.iscoroutine(res) or isfuture(res):
                yield from res

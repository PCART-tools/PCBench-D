    @asyncio.coroutine
    def _send(self, *args, **kwargs):
        for receiver in self._items:
            res = receiver(*args, **kwargs)
            if asyncio.iscoroutine(res) or isinstance(res, asyncio.Future):
                yield from res

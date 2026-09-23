    def __init__(self, coro, args, kwargs):
        self.coro = asyncio.coroutine(coro)
        self.args = args
        self.kwargs = kwargs

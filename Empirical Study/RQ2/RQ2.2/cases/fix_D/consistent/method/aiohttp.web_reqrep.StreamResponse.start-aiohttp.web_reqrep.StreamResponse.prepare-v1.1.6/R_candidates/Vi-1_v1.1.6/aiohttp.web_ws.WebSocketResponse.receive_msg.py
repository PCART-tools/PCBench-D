    @asyncio.coroutine
    def receive_msg(self):
        warnings.warn(
            'receive_msg() coroutine is deprecated. use receive() instead',
            DeprecationWarning)
        return (yield from self.receive())

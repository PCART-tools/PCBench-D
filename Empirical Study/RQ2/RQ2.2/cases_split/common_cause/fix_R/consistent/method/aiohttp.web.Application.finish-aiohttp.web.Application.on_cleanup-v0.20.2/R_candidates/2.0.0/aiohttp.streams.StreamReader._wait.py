    @asyncio.coroutine
    def _wait(self, func_name):
        # StreamReader uses a future to link the protocol feed_data() method
        # to a read coroutine. Running two read coroutines at the same time
        # would have an unexpected behaviour. It would not possible to know
        # which coroutine would get the next data.
        if self._waiter is not None:
            raise RuntimeError('%s() called while another coroutine is '
                               'already waiting for incoming data' % func_name)

        waiter = self._waiter = helpers.create_future(self._loop)
        try:
            if self._timer:
                with self._timer:
                    yield from waiter
            else:
                yield from waiter
        finally:
            self._waiter = None

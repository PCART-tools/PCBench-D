    @asyncio.coroutine
    def release(self):
        """Reads all the body parts to the void till the final boundary."""
        while not self._at_eof:
            item = yield from self.next()
            if item is None:
                break
            yield from item.release()

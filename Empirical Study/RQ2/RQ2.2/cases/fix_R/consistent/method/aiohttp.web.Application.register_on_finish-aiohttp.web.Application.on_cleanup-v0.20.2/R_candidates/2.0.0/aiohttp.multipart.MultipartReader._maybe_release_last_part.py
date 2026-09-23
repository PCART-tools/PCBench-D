    @asyncio.coroutine
    def _maybe_release_last_part(self):
        """Ensures that the last read body part is read completely."""
        if self._last_part is not None:
            if not self._last_part.at_eof():
                yield from self._last_part.release()
            self._unread.extend(self._last_part._unread)
            self._last_part = None

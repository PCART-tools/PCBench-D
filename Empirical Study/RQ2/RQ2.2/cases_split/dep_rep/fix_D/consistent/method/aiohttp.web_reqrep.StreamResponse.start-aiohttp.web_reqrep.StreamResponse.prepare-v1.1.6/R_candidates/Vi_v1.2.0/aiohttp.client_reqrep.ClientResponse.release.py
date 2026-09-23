    @asyncio.coroutine
    def release(self):
        if self._closed:
            return
        try:
            content = self.content
            if content is not None:
                while not content.at_eof():
                    yield from content.readany()
        except Exception:
            self._connection.close()
            self._connection = None
            raise
        finally:
            self._closed = True
            if self._connection is not None:
                self._connection.release()
                if self._reader is not None:
                    self._reader.unset_parser()
                self._connection = None
            self._cleanup_writer()
            self._notify_content()

    @asyncio.coroutine
    def _sendfile_fallback(self, request, fobj, count):
        # Mimic the _sendfile_system() method, but without using the
        # os.sendfile() system call. This should be used on systems
        # that don't support the os.sendfile().

        # To avoid blocking the event loop & to keep memory usage low,
        # fobj is transferred in chunks controlled by the
        # constructor's chunk_size argument.

        writer = (yield from super().prepare(request))

        self.set_tcp_cork(True)
        try:
            chunk_size = self._chunk_size

            chunk = fobj.read(chunk_size)
            while True:
                yield from writer.write(chunk)
                count = count - chunk_size
                if count <= 0:
                    break
                chunk = fobj.read(min(chunk_size, count))
        finally:
            self.set_tcp_nodelay(True)

        yield from writer.drain()
        return writer

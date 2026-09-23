    @asyncio.coroutine
    def sendfile(self, fobj, count):
        if self._transport is None:
            if self._drain_waiter is None:
                self._drain_waiter = create_future(self.loop)

            yield from self._drain_waiter

        out_socket = self._transport.get_extra_info("socket").dup()
        out_socket.setblocking(False)
        out_fd = out_socket.fileno()
        in_fd = fobj.fileno()
        offset = fobj.tell()

        loop = self.loop
        try:
            yield from loop.sock_sendall(out_socket, b''.join(self._buffer))
            fut = create_future(loop)
            self._sendfile_cb(fut, out_fd, in_fd, offset, count, loop, False)
            yield from fut
        finally:
            out_socket.close()

        self.output_size += count
        self._transport = None
        self._stream.release()

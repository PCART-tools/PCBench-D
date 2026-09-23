    async def sendfile(self, fobj, count):
        out_socket = self.transport.get_extra_info('socket').dup()
        out_socket.setblocking(False)
        out_fd = out_socket.fileno()
        in_fd = fobj.fileno()
        offset = fobj.tell()

        loop = self.loop
        data = b''.join(self._sendfile_buffer)
        try:
            await loop.sock_sendall(out_socket, data)
            fut = loop.create_future()
            self._sendfile_cb(fut, out_fd, in_fd, offset, count, loop, False)
            await fut
        except Exception:
            server_logger.debug('Socket error')
            self.transport.close()
        finally:
            out_socket.close()

        self.output_size += count
        await super().write_eof()

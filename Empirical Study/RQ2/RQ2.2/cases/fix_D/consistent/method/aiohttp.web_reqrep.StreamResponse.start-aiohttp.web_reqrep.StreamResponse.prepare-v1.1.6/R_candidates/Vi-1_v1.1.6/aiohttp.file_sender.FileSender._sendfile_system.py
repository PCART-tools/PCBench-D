    @asyncio.coroutine
    def _sendfile_system(self, request, resp, fobj, count):
        # Write count bytes of fobj to resp using
        # the os.sendfile system call.
        #
        # request should be a aiohttp.web.Request instance.
        #
        # resp should be a aiohttp.web.StreamResponse instance.
        #
        # fobj should be an open file object.
        #
        # count should be an integer > 0.

        transport = request.transport

        if transport.get_extra_info("sslcontext"):
            yield from self._sendfile_fallback(request, resp, fobj, count)
            return

        def _send_headers(resp_impl):
            # Durty hack required for
            # https://github.com/KeepSafe/aiohttp/issues/1093
            # don't send headers in sendfile mode
            pass

        resp._send_headers = _send_headers

        @asyncio.coroutine
        def write_eof():
            # Durty hack required for
            # https://github.com/KeepSafe/aiohttp/issues/1177
            # do nothing in write_eof
            pass

        resp.write_eof = write_eof

        resp_impl = yield from resp.prepare(request)

        loop = request.app.loop
        # See https://github.com/KeepSafe/aiohttp/issues/958 for details

        # send headers
        headers = ['HTTP/{0.major}.{0.minor} 200 OK\r\n'.format(
            request.version)]
        for hdr, val in resp.headers.items():
            headers.append('{}: {}\r\n'.format(hdr, val))
        headers.append('\r\n')

        out_socket = transport.get_extra_info("socket").dup()
        out_socket.setblocking(False)
        out_fd = out_socket.fileno()
        in_fd = fobj.fileno()

        bheaders = ''.join(headers).encode('utf-8')
        headers_length = len(bheaders)
        resp_impl.headers_length = headers_length
        resp_impl.output_length = headers_length + count

        try:
            yield from loop.sock_sendall(out_socket, bheaders)
            fut = create_future(loop)
            self._sendfile_cb(fut, out_fd, in_fd, 0, count, loop, False)

            yield from fut
        finally:
            out_socket.close()

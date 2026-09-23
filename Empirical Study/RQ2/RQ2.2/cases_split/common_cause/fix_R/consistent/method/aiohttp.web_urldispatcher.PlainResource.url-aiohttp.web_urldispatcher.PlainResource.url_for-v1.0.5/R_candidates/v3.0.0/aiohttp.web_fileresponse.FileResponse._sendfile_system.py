    async def _sendfile_system(self, request, fobj, count):
        # Write count bytes of fobj to resp using
        # the os.sendfile system call.
        #
        # For details check
        # https://github.com/KeepSafe/aiohttp/issues/1177
        # See https://github.com/KeepSafe/aiohttp/issues/958 for details
        #
        # request should be a aiohttp.web.Request instance.
        # fobj should be an open file object.
        # count should be an integer > 0.

        transport = request.transport
        if (transport.get_extra_info("sslcontext") or
                transport.get_extra_info("socket") is None):
            writer = await self._sendfile_fallback(request, fobj, count)
        else:
            writer = SendfileStreamWriter(
                request.protocol,
                transport,
                request.loop
            )
            request._payload_writer = writer

            await super().prepare(request)
            await writer.sendfile(fobj, count)

        return writer

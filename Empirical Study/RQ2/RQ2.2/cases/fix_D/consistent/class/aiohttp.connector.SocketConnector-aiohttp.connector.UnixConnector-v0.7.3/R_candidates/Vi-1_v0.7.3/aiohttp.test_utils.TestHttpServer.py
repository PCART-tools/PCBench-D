    class TestHttpServer(server.ServerHttpProtocol):

        def connection_made(self, transport):
            transports.append(transport)

            super().connection_made(transport)

        def handle_request(self, message, payload):
            if properties.get('close', False):
                return

            if properties.get('noresponse', False):
                yield from asyncio.sleep(99999)

            for hdr, val in message.headers:
                if (hdr == 'EXPECT') and (val == '100-continue'):
                    self.transport.write(b'HTTP/1.0 100 Continue\r\n\r\n')
                    break

            if router is not None:
                body = bytearray()
                try:
                    while True:
                        body.extend((yield from payload.read()))
                except aiohttp.EofStream:
                    pass

                rob = router(
                    self, properties, self.transport, message, bytes(body))
                rob.dispatch()

            else:
                response = aiohttp.Response(self.writer, 200, message.version)

                text = b'Test message'
                response.add_header('Content-type', 'text/plain')
                response.add_header('Content-length', str(len(text)))
                response.send_headers()
                response.write(text)
                response.write_eof()

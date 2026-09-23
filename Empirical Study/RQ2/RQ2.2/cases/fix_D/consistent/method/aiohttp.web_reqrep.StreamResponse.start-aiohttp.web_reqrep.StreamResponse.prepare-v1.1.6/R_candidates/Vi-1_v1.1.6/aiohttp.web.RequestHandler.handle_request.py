    @asyncio.coroutine
    def handle_request(self, message, payload):
        self._manager._requests_count += 1
        if self.access_log:
            now = self._loop.time()

        request = web_reqrep.Request(
            message, payload,
            self.transport, self.reader, self.writer,
            self._time_service,
            secure_proxy_ssl_header=self._secure_proxy_ssl_header)
        self._request = request
        try:
            match_info = yield from self._router.resolve(request)
            assert isinstance(match_info, AbstractMatchInfo), match_info
            match_info.add_app(self._app)
            match_info.freeze()

            resp = None
            request._match_info = match_info
            expect = request.headers.get(hdrs.EXPECT)
            if expect:
                resp = (
                    yield from match_info.expect_handler(request))

            if resp is None:
                handler = match_info.handler
                for app in match_info.apps:
                    for factory in reversed(app.middlewares):
                        handler = yield from factory(app, handler)
                resp = yield from handler(request)

            assert isinstance(resp, web_reqrep.StreamResponse), \
                ("Handler {!r} should return response instance, "
                 "got {!r} [middlewares {!r}]").format(
                     match_info.handler, type(resp), self._middlewares)
        except web_exceptions.HTTPException as exc:
            resp = exc

        resp_msg = yield from resp.prepare(request)
        yield from resp.write_eof()

        # notify server about keep-alive
        self.keep_alive(resp.keep_alive)

        # Restore default state.
        # Should be no-op if server code didn't touch these attributes.
        self.writer.set_tcp_cork(False)
        self.writer.set_tcp_nodelay(True)

        # log access
        if self.access_log:
            self.log_access(message, None, resp_msg, self._loop.time() - now)

        # for repr
        self._request = None

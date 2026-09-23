    @asyncio.coroutine
    def _handle(self, request):
        match_info = yield from self._router.resolve(request)
        assert isinstance(match_info, AbstractMatchInfo), match_info
        match_info.add_app(self)

        if __debug__:
            match_info.freeze()

        resp = None
        request._match_info = match_info
        expect = request.headers.get(hdrs.EXPECT)
        if expect:
            resp = yield from match_info.expect_handler(request)
            yield from request.writer.drain()

        if resp is None:
            handler = match_info.handler
            for app in match_info.apps[::-1]:
                for m, new_style in app._middlewares:
                    if new_style:
                        handler = partial(m, handler=handler)
                    else:
                        handler = yield from m(app, handler)

            resp = yield from handler(request)

        assert isinstance(resp, web_response.StreamResponse), \
            ("Handler {!r} should return response instance, "
             "got {!r} [middlewares {!r}]").format(
                 match_info.handler, type(resp),
                 [middleware
                  for app in match_info.apps
                  for middleware in app.middlewares])
        return resp

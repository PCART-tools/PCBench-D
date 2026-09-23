    async def _handle(self, request):
        match_info = await self._router.resolve(request)
        assert isinstance(match_info, AbstractMatchInfo), match_info
        match_info.add_app(self)

        if __debug__:
            match_info.freeze()

        resp = None
        request._match_info = match_info
        expect = request.headers.get(hdrs.EXPECT)
        if expect:
            resp = await match_info.expect_handler(request)
            await request.writer.drain()

        if resp is None:
            handler = match_info.handler

            if self._run_middlewares:
                for app in match_info.apps[::-1]:
                    for m, new_style in app._middlewares_handlers:
                        if new_style:
                            handler = partial(m, handler=handler)
                        else:
                            handler = await m(app, handler)

            resp = await handler(request)

        assert isinstance(resp, StreamResponse), \
            ("Handler {!r} should return response instance, "
             "got {!r} [middlewares {!r}]").format(
                 match_info.handler, type(resp),
                 [middleware
                  for app in match_info.apps
                  for middleware in app.middlewares])
        return resp

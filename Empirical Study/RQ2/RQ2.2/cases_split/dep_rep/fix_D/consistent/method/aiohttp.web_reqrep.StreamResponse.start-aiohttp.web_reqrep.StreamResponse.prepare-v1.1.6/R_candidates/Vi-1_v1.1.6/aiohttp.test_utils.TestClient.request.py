    @asyncio.coroutine
    def request(self, method, path, *args, **kwargs):
        """Routes a request to the http server.

        The interface is identical to asyncio.ClientSession.request,
        except the loop kwarg is overridden by the instance used by the
        application.

        """
        resp = yield from self._session.request(
            method, self.make_url(path), *args, **kwargs
        )
        # save it to close later
        self._responses.append(resp)
        return resp

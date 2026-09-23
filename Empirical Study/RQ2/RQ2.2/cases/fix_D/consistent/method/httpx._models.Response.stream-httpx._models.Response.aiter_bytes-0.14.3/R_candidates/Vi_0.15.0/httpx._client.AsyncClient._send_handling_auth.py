    async def _send_handling_auth(
        self,
        request: Request,
        auth: Auth,
        timeout: Timeout,
        allow_redirects: bool,
        history: typing.List[Response],
    ) -> Response:
        auth_flow = auth.async_auth_flow(request)
        request = await auth_flow.__anext__()

        for hook in self._event_hooks["request"]:
            await hook(request)

        while True:
            response = await self._send_handling_redirects(
                request,
                timeout=timeout,
                allow_redirects=allow_redirects,
                history=history,
            )
            try:
                next_request = await auth_flow.asend(response)
            except StopAsyncIteration:
                return response
            except BaseException as exc:
                await response.aclose()
                raise exc from None
            else:
                response.history = list(history)
                await response.aread()
                request = next_request
                history.append(response)

    async def _send_handling_auth(
        self,
        request: Request,
        history: typing.List[Response],
        auth: Auth,
        timeout: Timeout,
    ) -> Response:
        if auth.requires_request_body:
            await request.aread()

        auth_flow = auth.auth_flow(request)
        request = next(auth_flow)
        while True:
            response = await self._send_single_request(request, timeout)
            if auth.requires_response_body:
                await response.aread()
            try:
                next_request = auth_flow.send(response)
            except StopIteration:
                return response
            except BaseException as exc:
                await response.aclose()
                raise exc from None
            else:
                response.history = list(history)
                await response.aread()
                request = next_request
                history.append(response)

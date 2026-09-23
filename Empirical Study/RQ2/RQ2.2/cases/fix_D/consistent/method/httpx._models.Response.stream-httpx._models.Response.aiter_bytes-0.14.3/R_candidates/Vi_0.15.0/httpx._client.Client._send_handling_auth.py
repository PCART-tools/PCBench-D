    def _send_handling_auth(
        self,
        request: Request,
        auth: Auth,
        timeout: Timeout,
        allow_redirects: bool,
        history: typing.List[Response],
    ) -> Response:
        auth_flow = auth.sync_auth_flow(request)
        request = next(auth_flow)

        for hook in self._event_hooks["request"]:
            hook(request)

        while True:
            response = self._send_handling_redirects(
                request,
                timeout=timeout,
                allow_redirects=allow_redirects,
                history=history,
            )
            try:
                next_request = auth_flow.send(response)
            except StopIteration:
                return response
            except BaseException as exc:
                response.close()
                raise exc from None
            else:
                response.history = list(history)
                response.read()
                request = next_request
                history.append(response)

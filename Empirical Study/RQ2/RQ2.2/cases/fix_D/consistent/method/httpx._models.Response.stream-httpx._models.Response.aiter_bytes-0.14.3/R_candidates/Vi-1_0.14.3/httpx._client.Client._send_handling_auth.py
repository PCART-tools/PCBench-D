    def _send_handling_auth(
        self,
        request: Request,
        history: typing.List[Response],
        auth: Auth,
        timeout: Timeout,
    ) -> Response:
        if auth.requires_request_body:
            request.read()

        auth_flow = auth.auth_flow(request)
        request = next(auth_flow)
        while True:
            response = self._send_single_request(request, timeout)
            if auth.requires_response_body:
                response.read()
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

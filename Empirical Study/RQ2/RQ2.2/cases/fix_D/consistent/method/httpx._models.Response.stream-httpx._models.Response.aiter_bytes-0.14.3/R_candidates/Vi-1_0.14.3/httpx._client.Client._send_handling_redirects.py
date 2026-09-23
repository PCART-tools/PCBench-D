    def _send_handling_redirects(
        self,
        request: Request,
        auth: Auth,
        timeout: Timeout,
        allow_redirects: bool = True,
        history: typing.List[Response] = None,
    ) -> Response:
        if history is None:
            history = []

        while True:
            if len(history) > self.max_redirects:
                raise TooManyRedirects(
                    "Exceeded maximum allowed redirects.", request=request
                )

            response = self._send_handling_auth(
                request, auth=auth, timeout=timeout, history=history
            )
            response.history = list(history)

            if not response.is_redirect:
                return response

            if allow_redirects:
                response.read()
            request = self._build_redirect_request(request, response)
            history = history + [response]

            if not allow_redirects:
                response.call_next = functools.partial(
                    self._send_handling_redirects,
                    request=request,
                    auth=auth,
                    timeout=timeout,
                    allow_redirects=False,
                    history=history,
                )
                return response

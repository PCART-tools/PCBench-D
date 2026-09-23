    def _send_handling_redirects(
        self,
        request: Request,
        timeout: Timeout,
        allow_redirects: bool,
        history: typing.List[Response],
    ) -> Response:
        while True:
            if len(history) > self.max_redirects:
                raise TooManyRedirects(
                    "Exceeded maximum allowed redirects.", request=request
                )

            response = self._send_single_request(request, timeout)
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
                    timeout=timeout,
                    allow_redirects=False,
                    history=history,
                )
                return response

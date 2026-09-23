    def send(
        self,
        request: Request,
        *,
        stream: bool = False,
        auth: typing.Union[AuthTypes, UnsetType] = UNSET,
        allow_redirects: bool = True,
        timeout: typing.Union[TimeoutTypes, UnsetType] = UNSET,
    ) -> Response:
        """
        Send a request.

        The request is sent as-is, unmodified.

        Typically you'll want to build one with `Client.build_request()`
        so that any client-level configuration is merged into the request,
        but passing an explicit `httpx.Request()` is supported as well.

        See also: [Request instances][0]

        [0]: /advanced/#request-instances
        """
        self._is_closed = False

        timeout = self.timeout if isinstance(timeout, UnsetType) else Timeout(timeout)

        auth = self._build_request_auth(request, auth)

        response = self._send_handling_auth(
            request,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            history=[],
        )

        if not stream:
            try:
                response.read()
            finally:
                response.close()

        try:
            for hook in self._event_hooks["response"]:
                hook(response)
        except Exception:
            response.close()
            raise

        return response

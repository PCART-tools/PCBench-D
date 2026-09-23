    async def _send_single_request(
        self, request: Request, timeout: Timeout
    ) -> Response:
        """
        Sends a single request, without handling any redirections.
        """
        transport = self._transport_for_url(request.url)

        with map_exceptions(HTTPCORE_EXC_MAP, request=request):
            (
                http_version,
                status_code,
                reason_phrase,
                headers,
                stream,
            ) = await transport.request(
                request.method.encode(),
                request.url.raw,
                headers=request.headers.raw,
                stream=request.stream,
                timeout=timeout.as_dict(),
            )
        response = Response(
            status_code,
            http_version=http_version.decode("ascii"),
            headers=headers,
            stream=stream,  # type: ignore
            request=request,
        )

        self.cookies.extract_cookies(response)

        status = f"{response.status_code} {response.reason_phrase}"
        response_line = f"{response.http_version} {status}"
        logger.debug(f'HTTP Request: {request.method} {request.url} "{response_line}"')

        return response

    def _redirect_stream(
        self, request: Request, method: str
    ) -> typing.Optional[ContentStream]:
        """
        Return the body that should be used for the redirect request.
        """
        if method != request.method and method == "GET":
            return None

        if not request.stream.can_replay():
            raise RequestBodyUnavailable(
                "Got a redirect response, but the request body was streaming "
                "and is no longer available.",
                request=request,
            )

        return request.stream

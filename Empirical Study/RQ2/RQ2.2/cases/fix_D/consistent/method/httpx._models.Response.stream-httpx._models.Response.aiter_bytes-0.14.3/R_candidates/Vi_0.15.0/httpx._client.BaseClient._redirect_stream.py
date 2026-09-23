    def _redirect_stream(
        self, request: Request, method: str
    ) -> typing.Optional[ByteStream]:
        """
        Return the body that should be used for the redirect request.
        """
        if method != request.method and method == "GET":
            return None

        return request.stream

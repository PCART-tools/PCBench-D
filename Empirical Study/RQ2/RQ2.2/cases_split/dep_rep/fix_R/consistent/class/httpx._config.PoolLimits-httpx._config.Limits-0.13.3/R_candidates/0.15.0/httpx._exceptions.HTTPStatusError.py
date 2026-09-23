class HTTPStatusError(HTTPError):
    """
    The response had an error HTTP status of 4xx or 5xx.

    May be raised when calling `response.raise_for_status()`
    """

    def __init__(
        self, message: str, *, request: "Request", response: "Response"
    ) -> None:
        super().__init__(message, request=request)
        self.response = response

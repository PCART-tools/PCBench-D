class RequestError(HTTPError):
    """
    Base class for all exceptions that may occur when issuing a `.request()`.
    """

    def __init__(self, message: str, *, request: "Request") -> None:
        super().__init__(message, request=request)

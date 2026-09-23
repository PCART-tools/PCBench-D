class ResponseClosed(StreamError):
    """
    Attempted to read or stream response content, but the request has been
    closed.
    """

    def __init__(self) -> None:
        message = (
            "Attempted to read or stream response content, but the request has "
            "been closed."
        )
        super().__init__(message)

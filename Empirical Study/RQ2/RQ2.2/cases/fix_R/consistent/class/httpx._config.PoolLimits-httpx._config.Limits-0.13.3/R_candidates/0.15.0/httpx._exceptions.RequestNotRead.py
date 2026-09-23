class RequestNotRead(StreamError):
    """
    Attempted to access request content, without having called `read()`.
    """

    def __init__(self) -> None:
        message = "Attempted to access request content, without having called `read()`."
        super().__init__(message)

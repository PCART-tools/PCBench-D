    def __init__(self) -> None:
        message = (
            "Attempted to read or stream response content, but the content has "
            "already been streamed."
        )
        super().__init__(message)

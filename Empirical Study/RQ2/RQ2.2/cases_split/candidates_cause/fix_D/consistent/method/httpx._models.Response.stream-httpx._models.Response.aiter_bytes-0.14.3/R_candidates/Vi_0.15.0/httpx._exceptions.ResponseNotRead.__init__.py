    def __init__(self) -> None:
        message = (
            "Attempted to access response content, without having called `read()` "
            "after a streaming response."
        )
        super().__init__(message)

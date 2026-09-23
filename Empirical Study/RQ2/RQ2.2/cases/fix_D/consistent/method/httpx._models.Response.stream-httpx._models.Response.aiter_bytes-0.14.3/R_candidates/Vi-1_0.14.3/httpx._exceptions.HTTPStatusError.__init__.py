    def __init__(
        self, message: str, *, request: "Request", response: "Response"
    ) -> None:
        super().__init__(message, request=request)
        self.response = response

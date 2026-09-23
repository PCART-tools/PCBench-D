    def __init__(self) -> None:
        message = (
            "Attempted to read or stream some content, but the content has "
            "already been streamed. For requests, this could be due to passing "
            "a generator as request content, and then receiving a redirect "
            "response or a secondary request as part of an authentication flow."
            "For responses, this could be due to attempting to stream the response "
            "content more than once."
        )
        super().__init__(message)

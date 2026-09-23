class LineLimitExceededParserError(ParserError):
    """Line is too long."""

    def __init__(self, msg, limit):
        super().__init__(msg)
        self.limit = limit

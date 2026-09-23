class InvalidURL(Exception):
    """
    URL is improperly formed or cannot be parsed.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)

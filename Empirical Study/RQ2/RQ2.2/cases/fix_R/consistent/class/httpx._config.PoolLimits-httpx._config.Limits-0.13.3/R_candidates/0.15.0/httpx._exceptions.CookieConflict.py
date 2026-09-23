class CookieConflict(Exception):
    """
    Attempted to lookup a cookie by name, but multiple cookies existed.

    Can occur when calling `response.cookies.get(...)`.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)

class NotRedirectResponse(Exception):
    """
    Response was not a redirect response.

    May be raised if `response.next()` is called without first
    properly checking `response.is_redirect`.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)

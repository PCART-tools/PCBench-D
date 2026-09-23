class HTTPError(Exception):
    """
    Base class for `RequestError` and `HTTPStatusError`.

    Useful for `try...except` blocks when issuing a request,
    and then calling `.raise_for_status()`.

    For example:

    ```
    try:
        response = httpx.get("https://www.example.com")
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"HTTP Exception for {exc.request.url} - {exc}")
    ```
    """

    def __init__(self, message: str, *, request: "Request") -> None:
        super().__init__(message)
        self.request = request

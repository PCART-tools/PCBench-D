    def __init__(
        self,
        app: Callable,
        raise_app_exceptions: bool = True,
        root_path: str = "",
        client: Tuple[str, int] = ("127.0.0.1", 123),
    ) -> None:
        self.app = app
        self.raise_app_exceptions = raise_app_exceptions
        self.root_path = root_path
        self.client = client

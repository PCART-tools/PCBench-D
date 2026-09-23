    def __init__(
        self, title: str = "PIL", width: int | None = None, height: int | None = None
    ) -> None:
        self.hwnd = Image.core.createwindow(
            title, self.__dispatcher, width or 0, height or 0
        )

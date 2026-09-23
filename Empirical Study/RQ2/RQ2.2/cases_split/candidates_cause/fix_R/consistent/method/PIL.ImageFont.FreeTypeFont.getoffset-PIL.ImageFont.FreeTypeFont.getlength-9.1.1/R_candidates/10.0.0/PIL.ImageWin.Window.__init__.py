    def __init__(self, title="PIL", width=None, height=None):
        self.hwnd = Image.core.createwindow(
            title, self.__dispatcher, width or 0, height or 0
        )

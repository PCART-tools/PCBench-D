    def __del__(self) -> None:
        try:
            name = self.__photo.name
        except AttributeError:
            return
        self.__photo.name = None
        try:
            self.__photo.tk.call("image", "delete", name)
        except Exception:
            pass  # ignore internal errors

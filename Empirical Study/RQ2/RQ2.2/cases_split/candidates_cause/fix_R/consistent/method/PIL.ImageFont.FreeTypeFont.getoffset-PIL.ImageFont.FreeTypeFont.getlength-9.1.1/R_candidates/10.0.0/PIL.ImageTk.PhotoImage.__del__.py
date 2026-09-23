    def __del__(self):
        name = self.__photo.name
        self.__photo.name = None
        try:
            self.__photo.tk.call("image", "delete", name)
        except Exception:
            pass  # ignore internal errors

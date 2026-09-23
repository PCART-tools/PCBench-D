    def tkPhotoImage(self) -> ImageTk.PhotoImage:
        from . import ImageTk

        return ImageTk.PhotoImage(self.convert2byte(), palette=256)

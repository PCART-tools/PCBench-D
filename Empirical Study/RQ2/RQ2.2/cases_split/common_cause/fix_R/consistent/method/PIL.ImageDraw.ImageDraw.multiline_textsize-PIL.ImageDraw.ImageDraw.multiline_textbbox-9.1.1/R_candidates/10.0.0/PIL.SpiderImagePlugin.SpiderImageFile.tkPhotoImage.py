    def tkPhotoImage(self):
        from . import ImageTk

        return ImageTk.PhotoImage(self.convert2byte(), palette=256)

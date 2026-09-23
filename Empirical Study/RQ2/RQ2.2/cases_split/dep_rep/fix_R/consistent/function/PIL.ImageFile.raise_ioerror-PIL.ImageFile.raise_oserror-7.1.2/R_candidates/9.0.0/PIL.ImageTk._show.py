def _show(image, title):
    """Helper for the Image.show method."""

    class UI(tkinter.Label):
        def __init__(self, master, im):
            if im.mode == "1":
                self.image = BitmapImage(im, foreground="white", master=master)
            else:
                self.image = PhotoImage(im, master=master)
            super().__init__(master, image=self.image, bg="black", bd=0)

    if not tkinter._default_root:
        raise OSError("tkinter not initialized")
    top = tkinter.Toplevel()
    if title:
        top.title(title)
    UI(top, image).pack()

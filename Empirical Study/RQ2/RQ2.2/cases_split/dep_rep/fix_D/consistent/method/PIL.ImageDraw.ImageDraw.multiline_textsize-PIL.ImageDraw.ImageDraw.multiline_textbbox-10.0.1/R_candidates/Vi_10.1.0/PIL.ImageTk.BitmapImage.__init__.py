    def __init__(self, image=None, **kw):
        # Tk compatibility: file or data
        if image is None:
            image = _get_image_from_kw(kw)

        self.__mode = image.mode
        self.__size = image.size

        if _pilbitmap_check():
            # fast way (requires the pilbitmap booster patch)
            image.load()
            kw["data"] = f"PIL:{image.im.id}"
            self.__im = image  # must keep a reference
        else:
            # slow but safe way
            kw["data"] = image.tobitmap()
        self.__photo = tkinter.BitmapImage(**kw)

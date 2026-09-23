    def __init__(self, image=None, size=None, **kw):
        # Tk compatibility: file or data
        if image is None:
            image = _get_image_from_kw(kw)

        if hasattr(image, "mode") and hasattr(image, "size"):
            # got an image instead of a mode
            mode = image.mode
            if mode == "P":
                # palette mapped data
                image.apply_transparency()
                image.load()
                try:
                    mode = image.palette.mode
                except AttributeError:
                    mode = "RGB"  # default
            size = image.size
            kw["width"], kw["height"] = size
        else:
            mode = image
            image = None

        if mode not in ["1", "L", "RGB", "RGBA"]:
            mode = Image.getmodebase(mode)

        self.__mode = mode
        self.__size = size
        self.__photo = tkinter.PhotoImage(**kw)
        self.tk = self.__photo.tk
        if image:
            self.paste(image)

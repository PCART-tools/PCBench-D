    def __init__(
        self,
        image: Image.Image | str | None = None,
        size: tuple[int, int] | None = None,
        **kw: Any,
    ) -> None:
        # Tk compatibility: file or data
        if image is None:
            image = _get_image_from_kw(kw)

        if image is None:
            msg = "Image is required"
            raise ValueError(msg)
        elif isinstance(image, str):
            mode = image
            image = None

            if size is None:
                msg = "If first argument is mode, size is required"
                raise ValueError(msg)
        else:
            # got an image instead of a mode
            mode = image.mode
            if mode == "P":
                # palette mapped data
                image.apply_transparency()
                image.load()
                mode = image.palette.mode if image.palette else "RGB"
            size = image.size
            kw["width"], kw["height"] = size

        if mode not in ["1", "L", "RGB", "RGBA"]:
            mode = Image.getmodebase(mode)

        self.__mode = mode
        self.__size = size
        self.__photo = tkinter.PhotoImage(**kw)
        self.tk = self.__photo.tk
        if image:
            self.paste(image)

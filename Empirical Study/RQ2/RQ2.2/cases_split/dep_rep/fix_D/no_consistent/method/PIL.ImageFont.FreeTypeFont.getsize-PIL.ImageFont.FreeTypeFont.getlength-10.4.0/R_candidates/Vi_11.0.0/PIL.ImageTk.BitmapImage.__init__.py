    def __init__(self, image: Image.Image | None = None, **kw: Any) -> None:
        # Tk compatibility: file or data
        if image is None:
            image = _get_image_from_kw(kw)

        if image is None:
            msg = "Image is required"
            raise ValueError(msg)
        self.__mode = image.mode
        self.__size = image.size

        self.__photo = tkinter.BitmapImage(data=image.tobitmap(), **kw)

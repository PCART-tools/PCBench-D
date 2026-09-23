    def __init__(
        self, image: Image.Image | str, size: tuple[int, int] | None = None
    ) -> None:
        if isinstance(image, str):
            mode = image
            image = ""
            if size is None:
                msg = "If first argument is mode, size is required"
                raise ValueError(msg)
        else:
            mode = image.mode
            size = image.size
        if mode not in ["1", "L", "P", "RGB"]:
            mode = Image.getmodebase(mode)
        self.image = Image.core.display(mode, size)
        self.mode = mode
        self.size = size
        if image:
            assert not isinstance(image, str)
            self.paste(image)

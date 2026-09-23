    def __init__(
        self,
        image: Image.Image | str,
        size: tuple[int, int] | list[int] | None = None,
        color: float | tuple[float, ...] | str | None = None,
    ) -> None:
        if isinstance(image, str):
            if size is None:
                msg = "If image argument is mode string, size must be a list or tuple"
                raise ValueError(msg)
            image = Image.new(image, size, color)
        self.draw = ImageDraw.Draw(image)
        self.image = image
        self.transform: tuple[float, float, float, float, float, float] | None = None

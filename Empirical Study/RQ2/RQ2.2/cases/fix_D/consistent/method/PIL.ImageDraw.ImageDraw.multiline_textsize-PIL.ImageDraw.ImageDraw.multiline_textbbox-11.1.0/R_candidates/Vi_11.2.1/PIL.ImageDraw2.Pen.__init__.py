    def __init__(self, color: str, width: int = 1, opacity: int = 255) -> None:
        self.color = ImageColor.getrgb(color)
        self.width = width

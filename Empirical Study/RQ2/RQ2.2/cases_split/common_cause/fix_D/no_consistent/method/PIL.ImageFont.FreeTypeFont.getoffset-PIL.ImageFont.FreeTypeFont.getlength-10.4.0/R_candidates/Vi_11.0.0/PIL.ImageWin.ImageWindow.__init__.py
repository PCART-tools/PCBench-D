    def __init__(self, image: Image.Image | Dib, title: str = "PIL") -> None:
        if not isinstance(image, Dib):
            image = Dib(image)
        self.image = image
        width, height = image.size
        super().__init__(title, width=width, height=height)

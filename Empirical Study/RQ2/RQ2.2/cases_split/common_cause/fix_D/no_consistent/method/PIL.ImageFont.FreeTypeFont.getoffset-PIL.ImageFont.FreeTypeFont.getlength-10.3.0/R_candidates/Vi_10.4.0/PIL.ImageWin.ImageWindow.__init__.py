    def __init__(self, image, title="PIL"):
        if not isinstance(image, Dib):
            image = Dib(image)
        self.image = image
        width, height = image.size
        super().__init__(title, width=width, height=height)

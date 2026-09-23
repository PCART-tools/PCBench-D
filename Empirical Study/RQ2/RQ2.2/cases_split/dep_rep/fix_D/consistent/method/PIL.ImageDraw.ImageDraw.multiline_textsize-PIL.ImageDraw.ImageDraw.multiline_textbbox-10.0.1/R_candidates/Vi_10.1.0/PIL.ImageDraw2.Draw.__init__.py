    def __init__(self, image, size=None, color=None):
        if not hasattr(image, "im"):
            image = Image.new(image, size, color)
        self.draw = ImageDraw.Draw(image)
        self.image = image
        self.transform = None

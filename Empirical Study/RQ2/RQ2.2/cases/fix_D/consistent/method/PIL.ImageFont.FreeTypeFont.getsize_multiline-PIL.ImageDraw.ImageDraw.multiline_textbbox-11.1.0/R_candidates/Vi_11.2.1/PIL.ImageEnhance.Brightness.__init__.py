    def __init__(self, image: Image.Image) -> None:
        self.image = image
        self.degenerate = Image.new(image.mode, image.size, 0)

        if "A" in image.getbands():
            self.degenerate.putalpha(image.getchannel("A"))

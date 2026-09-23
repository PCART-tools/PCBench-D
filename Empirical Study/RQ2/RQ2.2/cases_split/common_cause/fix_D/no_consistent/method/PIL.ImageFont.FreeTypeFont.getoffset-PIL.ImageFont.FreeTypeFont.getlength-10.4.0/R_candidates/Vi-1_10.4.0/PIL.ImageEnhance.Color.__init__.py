    def __init__(self, image: Image.Image) -> None:
        self.image = image
        self.intermediate_mode = "L"
        if "A" in image.getbands():
            self.intermediate_mode = "LA"

        self.degenerate = image.convert(self.intermediate_mode).convert(image.mode)

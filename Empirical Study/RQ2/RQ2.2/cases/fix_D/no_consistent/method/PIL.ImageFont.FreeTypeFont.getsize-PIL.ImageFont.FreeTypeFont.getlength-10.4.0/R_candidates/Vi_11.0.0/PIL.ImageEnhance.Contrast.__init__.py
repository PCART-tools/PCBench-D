    def __init__(self, image: Image.Image) -> None:
        self.image = image
        if image.mode != "L":
            image = image.convert("L")
        mean = int(ImageStat.Stat(image).mean[0] + 0.5)
        self.degenerate = Image.new("L", image.size, mean)
        if self.degenerate.mode != self.image.mode:
            self.degenerate = self.degenerate.convert(self.image.mode)

        if "A" in self.image.getbands():
            self.degenerate.putalpha(self.image.getchannel("A"))

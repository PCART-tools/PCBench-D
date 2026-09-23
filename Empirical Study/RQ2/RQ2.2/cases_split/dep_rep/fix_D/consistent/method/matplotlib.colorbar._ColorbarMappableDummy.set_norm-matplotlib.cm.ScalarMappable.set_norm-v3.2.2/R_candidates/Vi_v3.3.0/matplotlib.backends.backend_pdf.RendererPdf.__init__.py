    def __init__(self, file, image_dpi, height, width):
        super().__init__(width, height)
        self.file = file
        self.gc = self.new_gc()
        self.mathtext_parser = MathTextParser("Pdf")
        self.image_dpi = image_dpi

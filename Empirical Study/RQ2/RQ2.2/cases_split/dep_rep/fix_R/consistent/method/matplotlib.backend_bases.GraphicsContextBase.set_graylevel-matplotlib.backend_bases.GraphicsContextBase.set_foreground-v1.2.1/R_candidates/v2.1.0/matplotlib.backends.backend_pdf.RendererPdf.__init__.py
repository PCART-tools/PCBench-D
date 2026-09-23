    def __init__(self, file, image_dpi, height, width):
        RendererBase.__init__(self)
        self.height = height
        self.width = width
        self.file = file
        self.gc = self.new_gc()
        self.mathtext_parser = MathTextParser("Pdf")
        self.image_dpi = image_dpi

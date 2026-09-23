    def get_results(self, box, used_characters):
        _mathtext.ship(0, 0, box)
        return self._PDFResult(self.width,
                               self.height + self.depth,
                               self.depth,
                               self.glyphs,
                               self.rects,
                               used_characters)

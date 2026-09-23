    def get_results(self, box, used_characters):
        _mathtext.ship(0, 0, box)
        return (self.width,
                self.height + self.depth,
                self.depth,
                self.glyphs,
                self.rects)

    def get_results(self, box, used_characters):
        ship(0, 0, box)
        svg_elements = types.SimpleNamespace(svg_glyphs=self.svg_glyphs,
                                             svg_rects=self.svg_rects)
        return (self.width,
                self.height + self.depth,
                self.depth,
                svg_elements,
                used_characters)

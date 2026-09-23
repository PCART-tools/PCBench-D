    def get_required_width(self, renderer):
        """ Get width required for this cell. """
        l, b, w, h = self.get_text_bounds(renderer)
        return w * (1.0 + (2.0 * self.PAD))

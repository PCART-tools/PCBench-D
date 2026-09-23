    def get_font_names(self):
        """Return the list of available fonts."""
        return list(set([font.name for font in self.ttflist]))

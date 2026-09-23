    def get_text_bounds(self, renderer):
        """
        Return the text bounds as *(x, y, width, height)* in table coordinates.
        """
        return (self._text.get_window_extent(renderer)
                .transformed(self.get_data_transform().inverted())
                .bounds)

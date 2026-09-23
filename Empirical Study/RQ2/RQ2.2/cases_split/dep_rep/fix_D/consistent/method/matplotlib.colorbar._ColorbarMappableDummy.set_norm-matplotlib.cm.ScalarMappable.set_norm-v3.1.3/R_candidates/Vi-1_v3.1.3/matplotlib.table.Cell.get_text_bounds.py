    def get_text_bounds(self, renderer):
        """
        Return the text bounds as *(x, y, width, height)* in table coordinates.
        """
        bbox = self._text.get_window_extent(renderer)
        bboxa = bbox.inverse_transformed(self.get_data_transform())
        return bboxa.bounds

    def get_text_bounds(self, renderer):
        """ Get text bounds in axes co-ordinates. """
        bbox = self._text.get_window_extent(renderer)
        bboxa = bbox.inverse_transformed(self.get_data_transform())
        return bboxa.bounds

    @property
    def _rect_bbox(self):
        if self._drawtype == 'box':
            x0 = self._selection_artist.get_x()
            y0 = self._selection_artist.get_y()
            width = self._selection_artist.get_width()
            height = self._selection_artist.get_height()
            return x0, y0, width, height
        else:
            x, y = self._selection_artist.get_data()
            x0, x1 = min(x), max(x)
            y0, y1 = min(y), max(y)
            return x0, y0, x1 - x0, y1 - y0

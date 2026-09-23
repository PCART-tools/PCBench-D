    @property
    def _rect_bbox(self):
        if self._drawtype == 'box':
            x, y = self._selection_artist.center
            width = self._selection_artist.width
            height = self._selection_artist.height
            return x - width / 2., y - height / 2., width, height
        else:
            x, y = self._selection_artist.get_data()
            x0, x1 = min(x), max(x)
            y0, y1 = min(y), max(y)
            return x0, y0, x1 - x0, y1 - y0

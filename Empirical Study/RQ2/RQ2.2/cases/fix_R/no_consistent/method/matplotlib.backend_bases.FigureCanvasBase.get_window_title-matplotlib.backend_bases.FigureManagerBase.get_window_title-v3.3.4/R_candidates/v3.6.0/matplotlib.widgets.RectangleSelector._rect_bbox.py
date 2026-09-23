    @property
    def _rect_bbox(self):
        if self._drawtype == 'box':
            return self._selection_artist.get_bbox().bounds
        else:
            x, y = self._selection_artist.get_data()
            x0, x1 = min(x), max(x)
            y0, y1 = min(y), max(y)
            return x0, y0, x1 - x0, y1 - y0

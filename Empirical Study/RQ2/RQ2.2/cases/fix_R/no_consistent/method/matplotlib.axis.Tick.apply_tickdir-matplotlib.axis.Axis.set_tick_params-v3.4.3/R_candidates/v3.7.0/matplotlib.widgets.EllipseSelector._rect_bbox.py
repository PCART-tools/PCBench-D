    @property
    def _rect_bbox(self):
        x, y = self._selection_artist.center
        width = self._selection_artist.width
        height = self._selection_artist.height
        return x - width / 2., y - height / 2., width, height

    def _press(self, event):
        self.verts = [self._get_data(event)]
        self._selection_artist.set_visible(True)

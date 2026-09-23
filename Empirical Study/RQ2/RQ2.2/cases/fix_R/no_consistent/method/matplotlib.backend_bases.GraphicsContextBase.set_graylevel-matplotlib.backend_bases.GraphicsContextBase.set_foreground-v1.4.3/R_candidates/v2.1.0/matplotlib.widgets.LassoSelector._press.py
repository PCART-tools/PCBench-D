    def _press(self, event):
        self.verts = [self._get_data(event)]
        self.line.set_visible(True)

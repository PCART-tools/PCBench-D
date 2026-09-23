    def set_height(self, h):
        "Set the height of the rectangle."
        self._height = h
        self._update_y1()
        self.stale = True

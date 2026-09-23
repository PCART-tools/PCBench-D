    def set_width(self, w):
        "Set the width of the rectangle."
        self._width = w
        self._update_x1()
        self.stale = True

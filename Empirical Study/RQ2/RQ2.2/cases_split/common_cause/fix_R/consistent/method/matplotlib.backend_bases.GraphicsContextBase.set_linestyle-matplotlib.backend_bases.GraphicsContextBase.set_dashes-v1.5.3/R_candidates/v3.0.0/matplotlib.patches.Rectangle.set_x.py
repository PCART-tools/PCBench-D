    def set_x(self, x):
        "Set the left coord of the rectangle."
        self._x0 = x
        self._update_x1()
        self.stale = True

    def contains(self, mouseevent):
        if self._different_canvas(mouseevent):
            return False, {}
        if not self._check_xy(None):
            return False, {}
        return self.offsetbox.contains(mouseevent)

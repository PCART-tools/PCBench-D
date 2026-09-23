    def contains(self, mouseevent):
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        if not self._check_xy(None):
            return False, {}
        return self.offsetbox.contains(mouseevent)

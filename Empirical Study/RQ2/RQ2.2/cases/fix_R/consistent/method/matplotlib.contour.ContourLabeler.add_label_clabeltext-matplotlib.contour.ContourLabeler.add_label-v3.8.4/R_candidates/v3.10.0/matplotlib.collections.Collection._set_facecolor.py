    def _set_facecolor(self, c):
        if c is None:
            c = self._get_default_facecolor()

        self._facecolors = mcolors.to_rgba_array(c, self._alpha)
        self.stale = True

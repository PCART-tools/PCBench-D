    def _set_facecolor(self, c):
        if c is None:
            c = mpl.rcParams['patch.facecolor']

        self._is_filled = True
        try:
            if c.lower() == 'none':
                self._is_filled = False
        except AttributeError:
            pass
        self._facecolors = mcolors.to_rgba_array(c, self._alpha)
        self.stale = True

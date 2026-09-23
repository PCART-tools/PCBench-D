    def _set_edgecolor(self, c):
        set_hatch_color = True
        if c is None:
            if (mpl.rcParams['patch.force_edgecolor'] or
                    not self._is_filled or self._edge_default):
                c = mpl.rcParams['patch.edgecolor']
            else:
                c = 'none'
                set_hatch_color = False

        self._is_stroked = True
        try:
            if c.lower() == 'none':
                self._is_stroked = False
        except AttributeError:
            pass

        try:
            if c.lower() == 'face':   # Special case: lookup in "get" method.
                self._edgecolors = 'face'
                return
        except AttributeError:
            pass
        self._edgecolors = mcolors.to_rgba_array(c, self._alpha)
        if set_hatch_color and len(self._edgecolors):
            self._hatch_color = tuple(self._edgecolors[0])
        self.stale = True

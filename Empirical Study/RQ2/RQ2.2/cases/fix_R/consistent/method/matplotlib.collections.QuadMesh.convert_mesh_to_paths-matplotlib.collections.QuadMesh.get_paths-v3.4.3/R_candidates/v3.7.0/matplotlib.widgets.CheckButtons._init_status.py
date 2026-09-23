    def _init_status(self, actives):
        """
        Initialize properties to match active status.

        The user may have passed custom colours in *check_props* to the
        constructor, or to `.set_check_props`, so we need to modify the
        visibility after getting whatever the user set.
        """
        self._active_check_colors = self._checks.get_facecolor()
        if len(self._active_check_colors) == 1:
            self._active_check_colors = np.repeat(self._active_check_colors,
                                                  len(actives), axis=0)
        self._checks.set_facecolor(
            [ec if active else "none"
             for ec, active in zip(self._active_check_colors, actives)])

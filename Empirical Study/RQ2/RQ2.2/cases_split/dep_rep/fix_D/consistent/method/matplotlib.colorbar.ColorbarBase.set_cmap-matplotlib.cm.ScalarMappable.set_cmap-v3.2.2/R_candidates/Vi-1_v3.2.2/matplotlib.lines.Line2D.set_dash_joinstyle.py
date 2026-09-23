    def set_dash_joinstyle(self, s):
        """
        Set the join style for dashed lines.

        Parameters
        ----------
        s : {'miter', 'round', 'bevel'}
            For examples see :doc:`/gallery/lines_bars_and_markers/joinstyle`.
        """
        s = s.lower()
        cbook._check_in_list(self.validJoin, s=s)
        if self._dashjoinstyle != s:
            self.stale = True
        self._dashjoinstyle = s

    def set_dash_joinstyle(self, s):
        """
        Set the join style for dashed linestyles.

        Parameters
        ----------
        s : {'miter', 'round', 'bevel'}
        """
        s = s.lower()
        if s not in self.validJoin:
            raise ValueError('set_dash_joinstyle passed "%s";\n' % (s,)
                             + 'valid joinstyles are %s' % (self.validJoin,))
        if self._dashjoinstyle != s:
            self.stale = True
        self._dashjoinstyle = s

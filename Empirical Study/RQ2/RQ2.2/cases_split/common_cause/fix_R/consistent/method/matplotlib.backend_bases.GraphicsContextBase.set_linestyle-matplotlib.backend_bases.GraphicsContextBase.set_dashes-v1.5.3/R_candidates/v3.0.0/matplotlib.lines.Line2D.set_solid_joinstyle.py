    def set_solid_joinstyle(self, s):
        """
        Set the join style for solid linestyles.

        Parameters
        ----------
        s : {'miter', 'round', 'bevel'}
        """
        s = s.lower()
        if s not in self.validJoin:
            raise ValueError('set_solid_joinstyle passed "%s";\n' % (s,)
                             + 'valid joinstyles are %s' % (self.validJoin,))

        if self._solidjoinstyle != s:
            self.stale = True
        self._solidjoinstyle = s

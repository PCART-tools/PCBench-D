    def set_joinstyle(self, s):
        """
        Set the patch joinstyle

        Parameters
        ----------
        s : {'miter', 'round', 'bevel'}
        """
        s = s.lower()
        if s not in self.validJoin:
            raise ValueError('set_joinstyle passed "%s";\n' % (s,) +
                             'valid joinstyles are %s' % (self.validJoin,))
        self._joinstyle = s
        self.stale = True

    def set_capstyle(self, s):
        """
        Set the patch capstyle

        Parameters
        ----------
        s : {'butt', 'round', 'projecting'}
        """
        s = s.lower()
        if s not in self.validCap:
            raise ValueError('set_capstyle passed "%s";\n' % (s,) +
                             'valid capstyles are %s' % (self.validCap,))
        self._capstyle = s
        self.stale = True

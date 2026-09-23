    def set_solid_capstyle(self, s):
        """
        Set the cap style for solid linestyles

        ACCEPTS: ['butt' | 'round' |  'projecting']
        """
        s = s.lower()
        if s not in self.validCap:
            raise ValueError('set_solid_capstyle passed "%s";\n' % (s,)
                             + 'valid capstyles are %s' % (self.validCap,))
        if self._solidcapstyle != s:
            self.stale = True
        self._solidcapstyle = s

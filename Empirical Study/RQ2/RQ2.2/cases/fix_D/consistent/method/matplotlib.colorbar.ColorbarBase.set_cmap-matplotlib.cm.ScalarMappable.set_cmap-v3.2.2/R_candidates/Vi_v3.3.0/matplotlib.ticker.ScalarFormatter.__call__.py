    def __call__(self, x, pos=None):
        """
        Return the format for tick value *x* at position *pos*.
        """
        if len(self.locs) == 0:
            return ''
        else:
            xp = (x - self.offset) / (10. ** self.orderOfMagnitude)
            if abs(xp) < 1e-8:
                xp = 0
            if self._useLocale:
                s = locale.format_string(self.format, (xp,))
            else:
                s = self.format % xp
            return self.fix_minus(s)

    @cbook.deprecated("3.1")
    def pprint_val(self, x):
        xp = (x - self.offset) / (10. ** self.orderOfMagnitude)
        if np.abs(xp) < 1e-8:
            xp = 0
        if self._useLocale:
            return locale.format_string(self.format, (xp,))
        else:
            return self.format % xp

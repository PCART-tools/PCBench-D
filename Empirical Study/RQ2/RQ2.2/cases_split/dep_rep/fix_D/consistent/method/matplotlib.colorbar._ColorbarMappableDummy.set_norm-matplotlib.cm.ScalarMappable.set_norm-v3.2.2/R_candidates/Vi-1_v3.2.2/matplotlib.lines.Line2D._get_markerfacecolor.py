    def _get_markerfacecolor(self, alt=False):
        fc = self._markerfacecoloralt if alt else self._markerfacecolor
        if cbook._str_lower_equal(fc, 'auto'):
            if self.get_fillstyle() == 'none':
                return 'none'
            else:
                return self._color
        else:
            return fc

    def _get_markerfacecolor(self, alt=False):
        if alt:
            fc = self._markerfacecoloralt
        else:
            fc = self._markerfacecolor

        if (isinstance(fc, six.string_types) and fc.lower() == 'auto'):
            if self.get_fillstyle() == 'none':
                return 'none'
            else:
                return self._color
        else:
            return fc

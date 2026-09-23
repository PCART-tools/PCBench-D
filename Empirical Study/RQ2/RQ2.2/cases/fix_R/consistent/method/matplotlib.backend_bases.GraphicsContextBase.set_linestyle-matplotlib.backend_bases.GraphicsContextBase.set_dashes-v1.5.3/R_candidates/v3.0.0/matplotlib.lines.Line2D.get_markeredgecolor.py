    def get_markeredgecolor(self):
        mec = self._markeredgecolor
        if cbook._str_equal(mec, 'auto'):
            if rcParams['_internal.classic_mode']:
                if self._marker.get_marker() in ('.', ','):
                    return self._color
                if self._marker.is_filled() and self.get_fillstyle() != 'none':
                    return 'k'  # Bad hard-wired default...
            return self._color
        else:
            return mec

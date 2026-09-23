    def get_cursor_data(self, event):
        # docstring inherited
        x, y = event.xdata, event.ydata
        if (x < self._Ax[0] or x > self._Ax[-1] or
                y < self._Ay[0] or y > self._Ay[-1]):
            return None
        j = np.searchsorted(self._Ax, x) - 1
        i = np.searchsorted(self._Ay, y) - 1
        try:
            return self._A[i, j]
        except IndexError:
            return None

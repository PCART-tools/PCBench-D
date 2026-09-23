    def _set_label(self):
        if self.orientation == 'vertical':
            self.ax.set_ylabel(self._label, **self._labelkw)
        else:
            self.ax.set_xlabel(self._label, **self._labelkw)
        self.stale = True

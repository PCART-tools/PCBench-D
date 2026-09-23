    def __call__(self):
        show_all = True
        # Ensure previous behaviour with full circle non-annular views.
        if self._axes:
            if _is_full_circle_rad(*self._axes.viewLim.intervalx):
                rorigin = self._axes.get_rorigin() * self._axes.get_rsign()
                if self._axes.get_rmin() <= rorigin:
                    show_all = False
        if show_all:
            return self.base()
        else:
            return [tick for tick in self.base() if tick > rorigin]

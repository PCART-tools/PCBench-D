    @property
    def _dpi_ratio(self):
        # Not available on Qt4 or some older Qt5.
        try:
            # self.devicePixelRatio() returns 0 in rare cases
            return self.devicePixelRatio() or 1
        except AttributeError:
            return 1

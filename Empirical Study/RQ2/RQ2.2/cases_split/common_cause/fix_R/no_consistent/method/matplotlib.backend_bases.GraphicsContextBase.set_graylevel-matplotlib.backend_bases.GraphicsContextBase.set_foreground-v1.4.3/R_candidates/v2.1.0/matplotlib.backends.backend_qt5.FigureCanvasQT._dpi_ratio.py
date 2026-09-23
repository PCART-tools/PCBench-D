    @property
    def _dpi_ratio(self):
        # Not available on Qt4 or some older Qt5.
        try:
            return self.devicePixelRatio()
        except AttributeError:
            return 1

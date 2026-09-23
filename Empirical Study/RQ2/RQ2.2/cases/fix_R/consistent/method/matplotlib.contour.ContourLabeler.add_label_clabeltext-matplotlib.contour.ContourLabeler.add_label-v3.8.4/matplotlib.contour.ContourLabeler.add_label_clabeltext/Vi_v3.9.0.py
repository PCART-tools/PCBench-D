    @_api.deprecated("3.8", alternative="add_label")
    def add_label_clabeltext(self, x, y, rotation, lev, cvalue):
        """Add contour label with `.Text.set_transform_rotates_text`."""
        with cbook._setattr_cm(self, _use_clabeltext=True):
            self.add_label(x, y, rotation, lev, cvalue)

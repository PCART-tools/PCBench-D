    def add_label_clabeltext(self, x, y, rotation, lev, cvalue):
        """Add contour label with `.Text.set_transform_rotates_text`."""
        self.add_label(x, y, rotation, lev, cvalue)
        # Grab the last added text, and reconfigure its rotation.
        t = self.labelTexts[-1]
        data_rotation, = self.axes.transData.inverted().transform_angles(
            [rotation], [[x, y]])
        t.set(rotation=data_rotation, transform_rotates_text=True)

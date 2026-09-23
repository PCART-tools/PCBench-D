    def get_rotation(self):
        """Return the text angle in degrees between 0 and 360."""
        if self.get_transform_rotates_text():
            return self.get_transform().transform_angles(
                [self._rotation], [self.get_unitless_position()]).item(0)
        else:
            return self._rotation

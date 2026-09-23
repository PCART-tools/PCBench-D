    def get_rotation(self):
        """Return the text angle in degrees between 0 and 360."""
        if self.get_transform_rotates_text():
            angle = get_rotation(self._rotation)
            x, y = self.get_unitless_position()
            angles = [angle, ]
            pts = [[x, y]]
            return self.get_transform().transform_angles(angles, pts).item(0)
        else:
            return get_rotation(self._rotation)  # string_or_number -> number

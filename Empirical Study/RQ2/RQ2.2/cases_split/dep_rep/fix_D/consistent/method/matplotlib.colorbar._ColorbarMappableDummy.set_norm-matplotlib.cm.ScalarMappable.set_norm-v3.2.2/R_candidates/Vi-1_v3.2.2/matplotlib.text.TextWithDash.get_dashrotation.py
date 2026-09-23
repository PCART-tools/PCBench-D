    def get_dashrotation(self):
        """
        Get the rotation of the dash in degrees.
        """
        if self._dashrotation is None:
            return self.get_rotation()
        else:
            return self._dashrotation

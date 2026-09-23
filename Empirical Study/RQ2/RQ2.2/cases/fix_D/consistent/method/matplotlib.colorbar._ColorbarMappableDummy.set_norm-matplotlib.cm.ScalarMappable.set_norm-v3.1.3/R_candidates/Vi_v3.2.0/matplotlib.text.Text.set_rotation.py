    def set_rotation(self, s):
        """
        Set the rotation of the text.

        Parameters
        ----------
        s : {angle in degrees, 'vertical', 'horizontal'}
        """
        self._rotation = s
        self.stale = True

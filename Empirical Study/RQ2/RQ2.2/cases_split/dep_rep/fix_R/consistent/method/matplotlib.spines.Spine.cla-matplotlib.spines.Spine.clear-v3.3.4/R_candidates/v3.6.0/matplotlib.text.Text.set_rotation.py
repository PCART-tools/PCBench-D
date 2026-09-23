    def set_rotation(self, s):
        """
        Set the rotation of the text.

        Parameters
        ----------
        s : float or {'vertical', 'horizontal'}
            The rotation angle in degrees in mathematically positive direction
            (counterclockwise). 'horizontal' equals 0, 'vertical' equals 90.
        """
        if isinstance(s, Real):
            self._rotation = float(s) % 360
        elif cbook._str_equal(s, 'horizontal') or s is None:
            self._rotation = 0.
        elif cbook._str_equal(s, 'vertical'):
            self._rotation = 90.
        else:
            raise ValueError("rotation must be 'vertical', 'horizontal' or "
                             f"a number, not {s}")
        self.stale = True

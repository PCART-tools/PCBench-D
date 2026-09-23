    def get_axes_pad(self):
        """
        Return the axes padding.

        Returns
        -------
        hpad, vpad
            Padding (horizontal pad, vertical pad) in inches.
        """
        return (self._horiz_pad_size.fixed_size,
                self._vert_pad_size.fixed_size)

    def set_axes_pad(self, axes_pad):
        """
        Set the padding between the axes.

        Parameters
        ----------
        axes_pad : (float, float)
            The padding (horizontal pad, vertical pad) in inches.
        """
        self._horiz_pad_size.fixed_size = axes_pad[0]
        self._vert_pad_size.fixed_size = axes_pad[1]

    def set_alignment(self, align):
        """
        Set if axes spine and labels are drawn at top or bottom (or left/right)
        of the axes.

        Parameters
        ----------
        align : str
            either 'top' or 'bottom' for orientation='x' or
            'left' or 'right' for orientation='y' axis.
        """
        cbook._check_in_list(self._locstrings, align=align)
        if align == self._locstrings[1]:  # Need to change the orientation.
            self._locstrings = self._locstrings[::-1]
        self.spines[self._locstrings[0]].set_visible(True)
        self.spines[self._locstrings[1]].set_visible(False)
        self._axis.set_ticks_position(align)
        self._axis.set_label_position(align)

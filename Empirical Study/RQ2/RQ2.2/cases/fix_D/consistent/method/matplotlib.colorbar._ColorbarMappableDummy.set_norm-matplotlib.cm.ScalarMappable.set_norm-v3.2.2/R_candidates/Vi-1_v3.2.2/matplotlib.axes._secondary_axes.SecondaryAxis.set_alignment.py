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
        if align in self._locstrings:
            if align == self._locstrings[1]:
                # need to change the orientation.
                self._locstrings = self._locstrings[::-1]
            elif align != self._locstrings[0]:
                raise ValueError('"{}" is not a valid axis orientation, '
                                 'not changing the orientation;'
                                 'choose "{}" or "{}""'.format(align,
                                 self._locstrings[0], self._locstrings[1]))
            self.spines[self._locstrings[0]].set_visible(True)
            self.spines[self._locstrings[1]].set_visible(False)
            self._axis.set_ticks_position(align)
            self._axis.set_label_position(align)

    def set_width_ratios(self, width_ratios):
        """
        Set the relative widths of the columns.

        *width_ratios* must be of length *ncols*. Each column gets a relative
        width of ``width_ratios[i] / sum(width_ratios)``.
        """
        if width_ratios is not None and len(width_ratios) != self._ncols:
            raise ValueError('Expected the given number of width ratios to '
                             'match the number of columns of the grid')
        self._col_width_ratios = width_ratios

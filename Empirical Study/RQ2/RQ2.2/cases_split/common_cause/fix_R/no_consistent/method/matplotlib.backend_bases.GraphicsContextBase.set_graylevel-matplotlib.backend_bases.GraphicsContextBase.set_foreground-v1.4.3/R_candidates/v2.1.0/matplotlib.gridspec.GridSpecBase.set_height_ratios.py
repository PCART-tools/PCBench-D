    def set_height_ratios(self, height_ratios):
        if height_ratios is not None and len(height_ratios) != self._nrows:
            raise ValueError('Expected the given number of height ratios to '
                             'match the number of rows of the grid')
        self._row_height_ratios = height_ratios

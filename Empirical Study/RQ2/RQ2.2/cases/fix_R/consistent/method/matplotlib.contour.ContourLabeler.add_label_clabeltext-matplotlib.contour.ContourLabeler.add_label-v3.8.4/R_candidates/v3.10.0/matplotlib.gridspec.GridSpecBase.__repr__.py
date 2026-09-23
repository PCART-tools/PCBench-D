    def __repr__(self):
        height_arg = (f', height_ratios={self._row_height_ratios!r}'
                      if len(set(self._row_height_ratios)) != 1 else '')
        width_arg = (f', width_ratios={self._col_width_ratios!r}'
                     if len(set(self._col_width_ratios)) != 1 else '')
        return '{clsname}({nrows}, {ncols}{optionals})'.format(
            clsname=self.__class__.__name__,
            nrows=self._nrows,
            ncols=self._ncols,
            optionals=height_arg + width_arg,
            )

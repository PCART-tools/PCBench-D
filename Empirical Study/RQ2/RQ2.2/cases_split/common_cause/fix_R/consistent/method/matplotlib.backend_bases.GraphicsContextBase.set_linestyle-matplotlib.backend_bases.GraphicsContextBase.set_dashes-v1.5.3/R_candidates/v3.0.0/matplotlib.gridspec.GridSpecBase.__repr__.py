    def __repr__(self):
        height_arg = (', height_ratios=%r' % self._row_height_ratios
                      if self._row_height_ratios is not None else '')
        width_arg = (', width_ratios=%r' % self._col_width_ratios
                     if self._col_width_ratios is not None else '')
        return '{clsname}({nrows}, {ncols}{optionals})'.format(
            clsname=self.__class__.__name__,
            nrows=self._nrows,
            ncols=self._ncols,
            optionals=height_arg + width_arg,
            )

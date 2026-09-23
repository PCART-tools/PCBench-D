    def auto_set_column_width(self, col):
        """
        Automatically set the widths of given columns to optimal sizes.

        Parameters
        ----------
        col : int or sequence of ints
            The indices of the columns to auto-scale.
        """
        # check for col possibility on iteration
        try:
            iter(col)
        except (TypeError, AttributeError):
            self._autoColumns.append(col)
        else:
            for cell in col:
                self._autoColumns.append(cell)

        self.stale = True

    def auto_set_column_width(self, col):
        """ Given column indexs in either List, Tuple or int. Will be able to
        automatically set the columns into optimal sizes.

        Here is the example of the input, which triger automatic adjustment on
        columns to optimal size by given index numbers.
        -1: the row labling
        0: the 1st column
        1: the 2nd column

        Args:
            col(List): list of indexs
            >>>table.auto_set_column_width([-1,0,1])

            col(Tuple): tuple of indexs
            >>>table.auto_set_column_width((-1,0,1))

            col(int): index integer
            >>>table.auto_set_column_width(-1)
            >>>table.auto_set_column_width(0)
            >>>table.auto_set_column_width(1)
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

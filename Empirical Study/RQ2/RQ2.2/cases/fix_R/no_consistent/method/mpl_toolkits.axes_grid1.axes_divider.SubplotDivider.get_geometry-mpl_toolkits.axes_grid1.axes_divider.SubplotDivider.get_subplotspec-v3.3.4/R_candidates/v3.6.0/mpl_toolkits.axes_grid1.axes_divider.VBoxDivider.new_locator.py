    def new_locator(self, ny, ny1=None):
        """
        Create a new `AxesLocator` for the specified cell.

        Parameters
        ----------
        ny, ny1 : int
            Integers specifying the row-position of the
            cell. When *ny1* is None, a single *ny*-th row is
            specified. Otherwise location of rows spanning between *ny*
            to *ny1* (but excluding *ny1*-th row) is specified.
        """
        return AxesLocator(self, 0, ny, 1, ny1 if ny1 is not None else ny + 1)

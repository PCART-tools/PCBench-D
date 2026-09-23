    def new_locator(self, nx, nx1=None):
        """
        Create a new `AxesLocator` for the specified cell.

        Parameters
        ----------
        nx, nx1 : int
            Integers specifying the column-position of the
            cell. When *nx1* is None, a single *nx*-th column is
            specified. Otherwise location of columns spanning between *nx*
            to *nx1* (but excluding *nx1*-th column) is specified.
        """
        return AxesLocator(self, nx, 0, nx1 if nx1 is not None else nx + 1, 1)

    def new_locator(self, nx, ny, nx1=None, ny1=None):
        """
        Return a new `AxesLocator` for the specified cell.

        Parameters
        ----------
        nx, nx1 : int
            Integers specifying the column-position of the
            cell. When *nx1* is None, a single *nx*-th column is
            specified. Otherwise location of columns spanning between *nx*
            to *nx1* (but excluding *nx1*-th column) is specified.
        ny, ny1 : int
            Same as *nx* and *nx1*, but for row positions.
        """
        return AxesLocator(
            self, nx, ny,
            nx1 if nx1 is not None else nx + 1,
            ny1 if ny1 is not None else ny + 1)

    def __init__(self, axes_divider, nx, ny, nx1=None, ny1=None):
        """
        Parameters
        ----------
        axes_divider : AxesDivider
        nx, nx1 : int
            Integers specifying the column-position of the
            cell. When *nx1* is None, a single *nx*-th column is
            specified. Otherwise location of columns spanning between *nx*
            to *nx1* (but excluding *nx1*-th column) is specified.
        ny, ny1 : int
            Same as *nx* and *nx1*, but for row positions.
        """
        self._axes_divider = axes_divider

        _xrefindex = axes_divider._xrefindex
        _yrefindex = axes_divider._yrefindex

        self._nx, self._ny = nx - _xrefindex, ny - _yrefindex

        if nx1 is None:
            _api.warn_deprecated(
                "3.5", message="Support for passing nx1=None to mean nx+1 is "
                "deprecated since %(since)s; in a future version, nx1=None "
                "will mean 'up to the last cell'.")
            nx1 = nx + 1
        if ny1 is None:
            _api.warn_deprecated(
                "3.5", message="Support for passing ny1=None to mean ny+1 is "
                "deprecated since %(since)s; in a future version, ny1=None "
                "will mean 'up to the last cell'.")
            ny1 = ny + 1

        self._nx1 = nx1 - _xrefindex
        self._ny1 = ny1 - _yrefindex

    def update_from_data_xy(self, xy, ignore=None, updatex=True, updatey=True):
        """
        Update the bounds of the `Bbox` based on the passed in
        data.  After updating, the bounds will have positive *width*
        and *height*; *x0* and *y0* will be the minimal values.

        Parameters
        ----------
        xy : ndarray
            A numpy array of 2D points.

        ignore : bool, optional
           - When ``True``, ignore the existing bounds of the `Bbox`.
           - When ``False``, include the existing bounds of the `Bbox`.
           - When ``None``, use the last value passed to :meth:`ignore`.

        updatex, updatey : bool, default: True
            When ``True``, update the x/y values.
        """
        if len(xy) == 0:
            return

        path = Path(xy)
        self.update_from_path(path, ignore=ignore,
                              updatex=updatex, updatey=updatey)

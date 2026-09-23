    def update_from_data_xy(self, xy, ignore=None, updatex=True, updatey=True):
        """
        Update the bounds of the :class:`Bbox` based on the passed in
        data.  After updating, the bounds will have positive *width*
        and *height*; *x0* and *y0* will be the minimal values.

        *xy*: a numpy array of 2D points

        *ignore*:
           - when True, ignore the existing bounds of the :class:`Bbox`.
           - when False, include the existing bounds of the :class:`Bbox`.
           - when None, use the last value passed to :meth:`ignore`.

        *updatex*: when True, update the x values

        *updatey*: when True, update the y values
        """
        if len(xy) == 0:
            return

        path = Path(xy)
        self.update_from_path(path, ignore=ignore,
                                    updatex=updatex, updatey=updatey)

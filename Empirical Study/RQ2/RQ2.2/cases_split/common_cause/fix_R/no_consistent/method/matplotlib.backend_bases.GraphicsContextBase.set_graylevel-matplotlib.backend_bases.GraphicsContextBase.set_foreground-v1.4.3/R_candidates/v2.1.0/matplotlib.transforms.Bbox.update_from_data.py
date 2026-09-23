    @cbook.deprecated('2.0', alternative='update_from_data_xy')
    def update_from_data(self, x, y, ignore=None):
        """
        Update the bounds of the :class:`Bbox` based on the passed in
        data.  After updating, the bounds will have positive *width*
        and *height*; *x0* and *y0* will be the minimal values.

        *x*: a numpy array of *x*-values

        *y*: a numpy array of *y*-values

        *ignore*:
           - when True, ignore the existing bounds of the :class:`Bbox`.
           - when False, include the existing bounds of the :class:`Bbox`.
           - when None, use the last value passed to :meth:`ignore`.
        """
        warnings.warn(
            "update_from_data requires a memory copy -- please replace with "
            "update_from_data_xy")

        xy = np.hstack((x.reshape((len(x), 1)), y.reshape((len(y), 1))))
        return self.update_from_data_xy(xy, ignore)

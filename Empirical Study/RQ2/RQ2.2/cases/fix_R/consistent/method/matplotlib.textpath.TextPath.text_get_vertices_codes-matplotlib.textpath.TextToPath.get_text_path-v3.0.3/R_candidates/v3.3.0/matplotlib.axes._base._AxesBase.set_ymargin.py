    def set_ymargin(self, m):
        """
        Set padding of Y data limits prior to autoscaling.

        *m* times the data interval will be added to each
        end of that interval before it is used in autoscaling.
        For example, if your data is in the range [0, 2], a factor of
        ``m = 0.1`` will result in a range [-0.2, 2.2].

        Negative values -0.5 < m < 0 will result in clipping of the data range.
        I.e. for a data range [0, 2], a factor of ``m = -0.1`` will result in
        a range [0.2, 1.8].

        Parameters
        ----------
        m : float greater than -0.5
        """
        if m <= -0.5:
            raise ValueError("margin must be greater than -0.5")
        self._ymargin = m
        self._request_autoscale_view(scalex=False, scaley=True)
        self.stale = True

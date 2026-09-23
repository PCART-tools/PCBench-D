    def autoscale(self, enable=True, axis='both', tight=None):
        """
        Autoscale the axis view to the data (toggle).

        Convenience method for simple axis view autoscaling.
        It turns autoscaling on or off, and then,
        if autoscaling for either axis is on, it performs
        the autoscaling on the specified axis or axes.

        Parameters
        ----------
        enable : bool or None, default: True
            True turns autoscaling on, False turns it off.
            None leaves the autoscaling state unchanged.
        axis : {'both', 'x', 'y'}, default: 'both'
            Which axis to operate on.
        tight : bool or None, default: None
            If True, first set the margins to zero.  Then, this argument is
            forwarded to `autoscale_view` (regardless of its value); see the
            description of its behavior there.
        """
        if enable is None:
            scalex = True
            scaley = True
        else:
            scalex = False
            scaley = False
            if axis in ['x', 'both']:
                self._autoscaleXon = bool(enable)
                scalex = self._autoscaleXon
            if axis in ['y', 'both']:
                self._autoscaleYon = bool(enable)
                scaley = self._autoscaleYon
        if tight and scalex:
            self._xmargin = 0
        if tight and scaley:
            self._ymargin = 0
        self._request_autoscale_view(tight=tight, scalex=scalex, scaley=scaley)

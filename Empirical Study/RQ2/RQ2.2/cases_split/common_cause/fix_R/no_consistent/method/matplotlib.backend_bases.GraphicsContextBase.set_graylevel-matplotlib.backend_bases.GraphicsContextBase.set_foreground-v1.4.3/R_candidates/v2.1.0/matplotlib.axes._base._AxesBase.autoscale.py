    def autoscale(self, enable=True, axis='both', tight=None):
        """
        Autoscale the axis view to the data (toggle).

        Convenience method for simple axis view autoscaling.
        It turns autoscaling on or off, and then,
        if autoscaling for either axis is on, it performs
        the autoscaling on the specified axis or axes.

        *enable*: [True | False | None]
            True (default) turns autoscaling on, False turns it off.
            None leaves the autoscaling state unchanged.

        *axis*: ['x' | 'y' | 'both']
            which axis to operate on; default is 'both'

        *tight*: [True | False | None]
            If True, set view limits to data limits;
            if False, let the locator and margins expand the view limits;
            if None, use tight scaling if the only artist is an image,
            otherwise treat *tight* as False.
            The *tight* setting is retained for future autoscaling
            until it is explicitly changed.


        Returns None.
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
        self.autoscale_view(tight=tight, scalex=scalex, scaley=scaley)

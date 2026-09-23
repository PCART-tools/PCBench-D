    def autoscale(self, enable=True, axis='both', tight=None):
        """
        Autoscale the axis view to the data (toggle).

        Convenience method for simple axis view autoscaling.
        It turns autoscaling on or off, and then,
        if autoscaling for either axis is on, it performs
        the autoscaling on the specified axis or Axes.

        Parameters
        ----------
        enable : bool or None, default: True
            True turns autoscaling on, False turns it off.
            None leaves the autoscaling state unchanged.
        axis : {'both', 'x', 'y'}, default: 'both'
            The axis on which to operate.  (For 3D Axes, *axis* can also be set
            to 'z', and 'both' refers to all three axes.)
        tight : bool or None, default: None
            If True, first set the margins to zero.  Then, this argument is
            forwarded to `~.axes.Axes.autoscale_view` (regardless of
            its value); see the description of its behavior there.
        """
        if enable is None:
            scalex = True
            scaley = True
        else:
            if axis in ['x', 'both']:
                self.set_autoscalex_on(bool(enable))
                scalex = self.get_autoscalex_on()
            else:
                scalex = False
            if axis in ['y', 'both']:
                self.set_autoscaley_on(bool(enable))
                scaley = self.get_autoscaley_on()
            else:
                scaley = False
        if tight and scalex:
            self._xmargin = 0
        if tight and scaley:
            self._ymargin = 0
        if scalex:
            self._request_autoscale_view("x", tight=tight)
        if scaley:
            self._request_autoscale_view("y", tight=tight)

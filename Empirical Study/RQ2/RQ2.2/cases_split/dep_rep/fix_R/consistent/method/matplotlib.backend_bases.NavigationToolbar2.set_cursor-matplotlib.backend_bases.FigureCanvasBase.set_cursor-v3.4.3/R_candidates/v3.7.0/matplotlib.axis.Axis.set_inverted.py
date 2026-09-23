    def set_inverted(self, inverted):
        """
        Set whether this Axis is oriented in the "inverse" direction.

        The "normal" direction is increasing to the right for the x-axis and to
        the top for the y-axis; the "inverse" direction is increasing to the
        left for the x-axis and to the bottom for the y-axis.
        """
        a, b = self.get_view_interval()
        # cast to bool to avoid bad interaction between python 3.8 and np.bool_
        self._set_lim(*sorted((a, b), reverse=bool(inverted)), auto=None)

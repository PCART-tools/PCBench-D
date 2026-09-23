    def set_inverted(self, inverted):
        """
        Set whether the axis is oriented in the "inverse" direction.

        The "normal" direction is increasing to the right for the x-axis and to
        the top for the y-axis; the "inverse" direction is increasing to the
        left for the x-axis and to the bottom for the y-axis.
        """
        # Currently, must be implemented in subclasses using set_xlim/set_ylim
        # rather than generically using set_view_interval, so that shared
        # axes get updated as well.
        raise NotImplementedError('Derived must override')

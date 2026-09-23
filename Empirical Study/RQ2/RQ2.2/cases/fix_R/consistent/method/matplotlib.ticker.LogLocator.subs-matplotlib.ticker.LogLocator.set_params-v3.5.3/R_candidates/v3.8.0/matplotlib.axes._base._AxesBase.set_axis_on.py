    def set_axis_on(self):
        """
        Do not hide all visual components of the x- and y-axis.

        This reverts the effect of a prior `.set_axis_off()` call. Whether the
        individual axis decorations are drawn is controlled by their respective
        visibility settings.

        This is on by default.
        """
        self.axison = True
        self.stale = True

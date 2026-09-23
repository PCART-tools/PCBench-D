    def set_axis_off(self):
        """
        Turn the x- and y-axis off.

        This affects the axis lines, ticks, ticklabels, grid and axis labels.
        """
        self.axison = False
        self.stale = True

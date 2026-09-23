    def set_ticks(self, ticks, *, minor=False):
        """
        Set this Axis' tick locations.

        If necessary, the view limits of the Axis are expanded so that all
        given ticks are visible.

        Parameters
        ----------
        ticks : list of floats
            List of tick locations.
        minor : bool, default: False
            If ``False``, set the major ticks; if ``True``, the minor ticks.

        Notes
        -----
        The mandatory expansion of the view limits is an intentional design
        choice to prevent the surprise of a non-visible tick. If you need
        other limits, you should set the limits explicitly after setting the
        ticks.
        """
        # XXX if the user changes units, the information will be lost here
        ticks = self.convert_units(ticks)
        if self is self.axes.xaxis:
            shared = [
                ax.xaxis
                for ax in self.axes.get_shared_x_axes().get_siblings(self.axes)
            ]
        elif self is self.axes.yaxis:
            shared = [
                ax.yaxis
                for ax in self.axes.get_shared_y_axes().get_siblings(self.axes)
            ]
        elif hasattr(self.axes, "zaxis") and self is self.axes.zaxis:
            shared = [
                ax.zaxis
                for ax in self.axes._shared_z_axes.get_siblings(self.axes)
            ]
        else:
            shared = [self]
        for axis in shared:
            if len(ticks) > 1:
                xleft, xright = axis.get_view_interval()
                if xright > xleft:
                    axis.set_view_interval(min(ticks), max(ticks))
                else:
                    axis.set_view_interval(max(ticks), min(ticks))
        self.axes.stale = True
        if minor:
            self.set_minor_locator(mticker.FixedLocator(ticks))
            return self.get_minor_ticks(len(ticks))
        else:
            self.set_major_locator(mticker.FixedLocator(ticks))
            return self.get_major_ticks(len(ticks))

    def set_units(self, u):
        """
        Set the units for axis.

        Parameters
        ----------
        u : units tag

        Notes
        -----
        The units of any shared axis will also be updated.
        """
        if u == self.units:
            return
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
        else:
            shared = [self]
        for axis in shared:
            axis.units = u
            axis._update_axisinfo()
            axis.callbacks.process('units')
            axis.callbacks.process('units finalize')
            axis.stale = True

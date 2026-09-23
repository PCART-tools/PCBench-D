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
        for name, axis in self.axes._axis_map.items():
            if self is axis:
                shared = [
                    getattr(ax, f"{name}axis")
                    for ax
                    in self.axes._shared_axes[name].get_siblings(self.axes)]
                break
        else:
            shared = [self]
        for axis in shared:
            axis.units = u
            axis._update_axisinfo()
            axis.callbacks.process('units')
            axis.callbacks.process('units finalize')
            axis.stale = True

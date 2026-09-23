    def set_color(self, color):
        """
        Change the color of the secondary axes and all decorators.

        Parameters
        ----------
        color : color
        """
        axis = self._axis_map[self._orientation]
        axis.set_tick_params(colors=color)
        for spine in self.spines.values():
            if spine.axis is axis:
                spine.set_color(color)
        axis.label.set_color(color)

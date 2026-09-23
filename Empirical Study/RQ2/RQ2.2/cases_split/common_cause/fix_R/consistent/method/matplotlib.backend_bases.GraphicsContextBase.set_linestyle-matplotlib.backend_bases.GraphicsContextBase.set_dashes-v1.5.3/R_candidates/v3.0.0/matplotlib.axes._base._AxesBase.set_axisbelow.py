    def set_axisbelow(self, b):
        """
        Set the zorder for the axes ticks and gridlines.

        Parameters
        ----------
        b : bool or 'line'
            ``True`` corresponds to a zorder of 0.5, ``False`` to a zorder of
            2.5, and ``"line"`` to a zorder of 1.5.

        """
        self._axisbelow = axisbelow = validate_axisbelow(b)
        if axisbelow is True:
            zorder = 0.5
        elif axisbelow is False:
            zorder = 2.5
        elif axisbelow == "line":
            zorder = 1.5
        else:
            raise ValueError("Unexpected axisbelow value")
        for axis in self._get_axis_list():
            axis.set_zorder(zorder)
        self.stale = True

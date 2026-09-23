    def set_axisbelow(self, b):
        """
        Set whether axis ticks and gridlines are above or below most artists.

        This controls the zorder of the ticks and gridlines. For more
        information on the zorder see :doc:`/gallery/misc/zorder_demo`.

        Parameters
        ----------
        b : bool or 'line'
            Possible values:

            - *True* (zorder = 0.5): Ticks and gridlines are below all Artists.
            - 'line' (zorder = 1.5): Ticks and gridlines are above patches
              (e.g. rectangles, with default zorder = 1) but still below lines
              and markers (with their default zorder = 2).
            - *False* (zorder = 2.5): Ticks and gridlines are above patches
              and lines / markers.

        See Also
        --------
        get_axisbelow
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

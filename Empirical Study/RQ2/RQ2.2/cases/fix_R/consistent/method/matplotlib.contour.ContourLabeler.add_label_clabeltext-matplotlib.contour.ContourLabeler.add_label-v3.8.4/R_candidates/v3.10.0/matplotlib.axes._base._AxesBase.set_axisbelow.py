    def set_axisbelow(self, b):
        """
        Set whether axis ticks and gridlines are above or below most artists.

        This controls the zorder of the ticks and gridlines. For more
        information on the zorder see :doc:`/gallery/misc/zorder_demo`.

        Parameters
        ----------
        b : bool or 'line'
            Possible values:

            - *True* (zorder = 0.5): Ticks and gridlines are below patches and
              lines, though still above images.
            - 'line' (zorder = 1.5): Ticks and gridlines are above patches
              (e.g. rectangles, with default zorder = 1) but still below lines
              and markers (with their default zorder = 2).
            - *False* (zorder = 2.5): Ticks and gridlines are above patches
              and lines / markers.

        Notes
        -----
        For more control, call the `~.Artist.set_zorder` method of each axis.

        See Also
        --------
        get_axisbelow
        """
        # Check that b is True, False or 'line'
        self._axisbelow = axisbelow = validate_axisbelow(b)
        zorder = {
            True: 0.5,
            'line': 1.5,
            False: 2.5,
        }[axisbelow]
        for axis in self._axis_map.values():
            axis.set_zorder(zorder)
        self.stale = True

    def get_window_extent(self, *args, **kwargs):
        """
        Return the Axes bounding box in display space; *args* and *kwargs*
        are empty.

        This bounding box does not include the spines, ticks, ticklables,
        or other labels.  For a bounding box including these elements use
        `~matplotlib.axes.Axes.get_tightbbox`.

        See Also
        --------
        matplotlib.axes.Axes.get_tightbbox
        matplotlib.axis.Axis.get_tightbbox
        matplotlib.spines.Spine.get_window_extent
        """
        return self.bbox

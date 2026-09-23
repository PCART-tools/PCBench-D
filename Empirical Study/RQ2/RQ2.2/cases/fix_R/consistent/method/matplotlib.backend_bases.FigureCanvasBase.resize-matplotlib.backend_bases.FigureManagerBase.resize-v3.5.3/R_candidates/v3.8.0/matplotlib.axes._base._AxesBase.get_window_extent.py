    def get_window_extent(self, renderer=None):
        """
        Return the Axes bounding box in display space.

        This bounding box does not include the spines, ticks, ticklabels,
        or other labels.  For a bounding box including these elements use
        `~matplotlib.axes.Axes.get_tightbbox`.

        See Also
        --------
        matplotlib.axes.Axes.get_tightbbox
        matplotlib.axis.Axis.get_tightbbox
        matplotlib.spines.Spine.get_window_extent
        """
        return self.bbox

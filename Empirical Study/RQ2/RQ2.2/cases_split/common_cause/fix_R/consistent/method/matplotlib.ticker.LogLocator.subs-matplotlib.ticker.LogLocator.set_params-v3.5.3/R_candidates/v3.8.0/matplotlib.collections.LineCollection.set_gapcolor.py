    def set_gapcolor(self, gapcolor):
        """
        Set a color to fill the gaps in the dashed line style.

        .. note::

            Striped lines are created by drawing two interleaved dashed lines.
            There can be overlaps between those two, which may result in
            artifacts when using transparency.

            This functionality is experimental and may change.

        Parameters
        ----------
        gapcolor : color or list of colors or None
            The color with which to fill the gaps. If None, the gaps are
            unfilled.
        """
        self._original_gapcolor = gapcolor
        self._set_gapcolor(gapcolor)

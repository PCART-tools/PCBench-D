    def set_linestyle(self, ls):
        """
        Set the patch linestyle.

        ===========================   =================
        linestyle                     description
        ===========================   =================
        ``'-'`` or ``'solid'``        solid line
        ``'--'`` or  ``'dashed'``     dashed line
        ``'-.'`` or  ``'dashdot'``    dash-dotted line
        ``':'`` or ``'dotted'``       dotted line
        ===========================   =================

        Alternatively a dash tuple of the following form can be provided::

            (offset, onoffseq)

        where ``onoffseq`` is an even length tuple of on and off ink in points.

        Parameters
        ----------
        ls : {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
            The line style.
        """
        if ls is None:
            ls = "solid"
        self._linestyle = ls
        # get the unscaled dash pattern
        offset, ls = self._us_dashes = mlines._get_dash_pattern(ls)
        # scale the dash pattern by the linewidth
        self._dashoffset, self._dashes = mlines._scale_dashes(
            offset, ls, self._linewidth)
        self.stale = True

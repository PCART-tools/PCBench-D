    def set_linestyle(self, ls):
        """
        Set the linestyle(s) for the collection.

        ===========================   =================
        linestyle                     description
        ===========================   =================
        ``'-'`` or ``'solid'``        solid line
        ``'--'`` or  ``'dashed'``     dashed line
        ``'-.'`` or  ``'dashdot'``    dash-dotted line
        ``':'`` or ``'dotted'``       dotted line
        ===========================   =================

        Alternatively a dash tuple of the following form can be provided::

            (offset, onoffseq),

        where ``onoffseq`` is an even length tuple of on and off ink in points.

        Parameters
        ----------
        ls : {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
            The line style.
        """
        try:
            if isinstance(ls, str):
                ls = cbook.ls_mapper.get(ls, ls)
                dashes = [mlines._get_dash_pattern(ls)]
            else:
                try:
                    dashes = [mlines._get_dash_pattern(ls)]
                except ValueError:
                    dashes = [mlines._get_dash_pattern(x) for x in ls]

        except ValueError:
            raise ValueError(
                'Do not know how to convert {!r} to dashes'.format(ls))

        # get the list of raw 'unscaled' dash patterns
        self._us_linestyles = dashes

        # broadcast and scale the lw and dash patterns
        self._linewidths, self._linestyles = self._bcast_lwls(
            self._us_lw, self._us_linestyles)

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
        ls : str or tuple or list thereof
            Valid values for individual linestyles include {'-', '--', '-.',
            ':', '', (offset, on-off-seq)}. See `.Line2D.set_linestyle` for a
            complete description.
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

        except ValueError as err:
            raise ValueError('Do not know how to convert {!r} to '
                             'dashes'.format(ls)) from err

        # get the list of raw 'unscaled' dash patterns
        self._us_linestyles = dashes

        # broadcast and scale the lw and dash patterns
        self._linewidths, self._linestyles = self._bcast_lwls(
            self._us_lw, self._us_linestyles)

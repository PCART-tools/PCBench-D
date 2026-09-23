    def set_linestyle(self, ls):
        """
        Set the linestyle of the line (also accepts drawstyles,
        e.g., ``'steps--'``)


        ===========================   =================
        linestyle                     description
        ===========================   =================
        ``'-'`` or ``'solid'``        solid line
        ``'--'`` or  ``'dashed'``     dashed line
        ``'-.'`` or  ``'dashdot'``    dash-dotted line
        ``':'`` or ``'dotted'``       dotted line
        ``'None'``                    draw nothing
        ``' '``                       draw nothing
        ``''``                        draw nothing
        ===========================   =================

        'steps' is equivalent to 'steps-pre' and is maintained for
        backward-compatibility.

        Alternatively a dash tuple of the following form can be provided::

            (offset, onoffseq),

        where ``onoffseq`` is an even length tuple of on and off ink in points.

        .. seealso::

            :meth:`set_drawstyle`
               To set the drawing style (stepping) of the plot.

        Parameters
        ----------
        ls : {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
            The line style.
        """
        if isinstance(ls, str):
            ds, ls = self._split_drawstyle_linestyle(ls)
            if ds is not None:
                self.set_drawstyle(ds)

            if ls in [' ', '', 'none']:
                ls = 'None'

            if ls not in self._lineStyles:
                try:
                    ls = ls_mapper_r[ls]
                except KeyError:
                    raise ValueError("Invalid linestyle {!r}; see docs of "
                                     "Line2D.set_linestyle for valid values"
                                     .format(ls))
            self._linestyle = ls
        else:
            self._linestyle = '--'

        # get the unscaled dashes
        self._us_dashOffset, self._us_dashSeq = _get_dash_pattern(ls)
        # compute the linewidth scaled dashes
        self._dashOffset, self._dashSeq = _scale_dashes(
            self._us_dashOffset, self._us_dashSeq, self._linewidth)

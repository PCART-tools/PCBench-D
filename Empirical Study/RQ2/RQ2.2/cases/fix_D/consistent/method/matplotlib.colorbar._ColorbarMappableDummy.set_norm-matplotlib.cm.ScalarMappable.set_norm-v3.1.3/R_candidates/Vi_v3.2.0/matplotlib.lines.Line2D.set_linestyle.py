    def set_linestyle(self, ls):
        """
        Set the linestyle of the line.

        Parameters
        ----------
        ls : {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
            Possible values:

            - A string:

              ===============================   =================
              Linestyle                         Description
              ===============================   =================
              ``'-'`` or ``'solid'``            solid line
              ``'--'`` or  ``'dashed'``         dashed line
              ``'-.'`` or  ``'dashdot'``        dash-dotted line
              ``':'`` or ``'dotted'``           dotted line
              ``'None'`` or ``' '`` or ``''``   draw nothing
              ===============================   =================

              Optionally, the string may be preceded by a drawstyle, e.g.
              ``'steps--'``. See :meth:`set_drawstyle` for details.

            - Alternatively a dash tuple of the following form can be
              provided::

                  (offset, onoffseq)

              where ``onoffseq`` is an even length tuple of on and off ink
              in points. See also :meth:`set_dashes`.

            For examples see :doc:`/gallery/lines_bars_and_markers/linestyles`.
        """
        if isinstance(ls, str):
            ds, ls = self._split_drawstyle_linestyle(ls)
            if ds is not None:
                self.set_drawstyle(ds)

            if ls in [' ', '', 'none']:
                ls = 'None'

            cbook._check_in_list([*self._lineStyles, *ls_mapper_r], ls=ls)
            if ls not in self._lineStyles:
                ls = ls_mapper_r[ls]
            self._linestyle = ls
        else:
            self._linestyle = '--'

        # get the unscaled dashes
        self._us_dashOffset, self._us_dashSeq = _get_dash_pattern(ls)
        # compute the linewidth scaled dashes
        self._dashOffset, self._dashSeq = _scale_dashes(
            self._us_dashOffset, self._us_dashSeq, self._linewidth)

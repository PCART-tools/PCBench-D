    def get_subplot_params(self, fig=None):
        """Return a dictionary of subplot layout parameters.
        """

        if fig is None:
            hspace = rcParams["figure.subplot.hspace"]
            wspace = rcParams["figure.subplot.wspace"]
        else:
            hspace = fig.subplotpars.hspace
            wspace = fig.subplotpars.wspace

        if self._hspace is not None:
            hspace = self._hspace

        if self._wspace is not None:
            wspace = self._wspace

        figbox = self._subplot_spec.get_position(fig, return_all=False)
        left, bottom, right, top = figbox.extents

        from matplotlib.figure import SubplotParams
        sp = SubplotParams(left=left,
                           right=right,
                           bottom=bottom,
                           top=top,
                           wspace=wspace,
                           hspace=hspace)

        return sp

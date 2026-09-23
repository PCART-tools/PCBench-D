    def get_subplot_params(self, figure=None):
        """Return a dictionary of subplot layout parameters."""
        hspace = (self._hspace if self._hspace is not None
                  else figure.subplotpars.hspace if figure is not None
                  else rcParams["figure.subplot.hspace"])
        wspace = (self._wspace if self._wspace is not None
                  else figure.subplotpars.wspace if figure is not None
                  else rcParams["figure.subplot.wspace"])

        figbox = self._subplot_spec.get_position(figure)
        left, bottom, right, top = figbox.extents

        return mpl.figure.SubplotParams(left=left, right=right,
                                        bottom=bottom, top=top,
                                        wspace=wspace, hspace=hspace)

    def subplots_adjust(self, left=None, bottom=None, right=None, top=None,
                        wspace=None, hspace=None):
        """
        Adjust the subplot layout parameters.

        Unset parameters are left unmodified; initial values are given by
        :rc:`figure.subplot.[name]`.

        Parameters
        ----------
        left : float, optional
            The position of the left edge of the subplots,
            as a fraction of the figure width.
        right : float, optional
            The position of the right edge of the subplots,
            as a fraction of the figure width.
        bottom : float, optional
            The position of the bottom edge of the subplots,
            as a fraction of the figure height.
        top : float, optional
            The position of the top edge of the subplots,
            as a fraction of the figure height.
        wspace : float, optional
            The width of the padding between subplots,
            as a fraction of the average Axes width.
        hspace : float, optional
            The height of the padding between subplots,
            as a fraction of the average Axes height.
        """
        if self.get_constrained_layout():
            self.set_constrained_layout(False)
            _api.warn_external(
                "This figure was using constrained_layout, but that is "
                "incompatible with subplots_adjust and/or tight_layout; "
                "disabling constrained_layout.")
        self.subplotpars.update(left, bottom, right, top, wspace, hspace)
        for ax in self.axes:
            if isinstance(ax, SubplotBase):
                ax._set_position(ax.get_subplotspec().get_position(self))
        self.stale = True

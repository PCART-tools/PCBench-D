    def indicate_inset_zoom(self, inset_ax, **kwargs):
        """
        Add an inset indicator rectangle to the Axes based on the axis
        limits for an *inset_ax* and draw connectors between *inset_ax*
        and the rectangle.

        Warnings
        --------
        This method is experimental as of 3.0, and the API may change.

        Parameters
        ----------
        inset_ax : `.Axes`
            Inset Axes to draw connecting lines to.  Two lines are
            drawn connecting the indicator box to the inset Axes on corners
            chosen so as to not overlap with the indicator box.

        **kwargs
            Other keyword arguments are passed on to `.Axes.indicate_inset`

        Returns
        -------
        inset_indicator : `.inset.InsetIndicator`
            An artist which contains

            inset_indicator.rectangle : `.Rectangle`
                The indicator frame.

            inset_indicator.connectors : 4-tuple of `.patches.ConnectionPatch`
                The four connector lines connecting to (lower_left, upper_left,
                lower_right upper_right) corners of *inset_ax*. Two lines are
                set with visibility to *False*,  but the user can set the
                visibility to True if the automatic choice is not deemed correct.

            .. versionchanged:: 3.10
                Previously the rectangle and connectors tuple were returned.
        """

        return self.indicate_inset(None, inset_ax, **kwargs)

    @_docstring.interpd
    def indicate_inset(self, bounds=None, inset_ax=None, *, transform=None,
                       facecolor='none', edgecolor='0.5', alpha=0.5,
                       zorder=None, **kwargs):
        """
        Add an inset indicator to the Axes.  This is a rectangle on the plot
        at the position indicated by *bounds* that optionally has lines that
        connect the rectangle to an inset Axes (`.Axes.inset_axes`).

        Warnings
        --------
        This method is experimental as of 3.0, and the API may change.

        Parameters
        ----------
        bounds : [x0, y0, width, height], optional
            Lower-left corner of rectangle to be marked, and its width
            and height.  If not set, the bounds will be calculated from the
            data limits of *inset_ax*, which must be supplied.

        inset_ax : `.Axes`, optional
            An optional inset Axes to draw connecting lines to.  Two lines are
            drawn connecting the indicator box to the inset Axes on corners
            chosen so as to not overlap with the indicator box.

        transform : `.Transform`
            Transform for the rectangle coordinates. Defaults to
            ``ax.transAxes``, i.e. the units of *rect* are in Axes-relative
            coordinates.

        facecolor : :mpltype:`color`, default: 'none'
            Facecolor of the rectangle.

        edgecolor : :mpltype:`color`, default: '0.5'
            Color of the rectangle and color of the connecting lines.

        alpha : float or None, default: 0.5
            Transparency of the rectangle and connector lines.  If not
            ``None``, this overrides any alpha value included in the
            *facecolor* and *edgecolor* parameters.

        zorder : float, default: 4.99
            Drawing order of the rectangle and connector lines.  The default,
            4.99, is just below the default level of inset Axes.

        **kwargs
            Other keyword arguments are passed on to the `.Rectangle` patch:

            %(Rectangle:kwdoc)s

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
        # to make the Axes connectors work, we need to apply the aspect to
        # the parent Axes.
        self.apply_aspect()

        if transform is None:
            transform = self.transData
        kwargs.setdefault('label', '_indicate_inset')

        indicator_patch = minset.InsetIndicator(
            bounds, inset_ax=inset_ax,
            facecolor=facecolor, edgecolor=edgecolor, alpha=alpha,
            zorder=zorder, transform=transform, **kwargs)
        self.add_artist(indicator_patch)

        return indicator_patch

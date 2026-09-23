    @_docstring.dedent_interpd
    def indicate_inset(self, bounds, inset_ax=None, *, transform=None,
                       facecolor='none', edgecolor='0.5', alpha=0.5,
                       zorder=4.99, **kwargs):
        """
        Add an inset indicator to the Axes.  This is a rectangle on the plot
        at the position indicated by *bounds* that optionally has lines that
        connect the rectangle to an inset Axes (`.Axes.inset_axes`).

        Warnings
        --------
        This method is experimental as of 3.0, and the API may change.

        Parameters
        ----------
        bounds : [x0, y0, width, height]
            Lower-left corner of rectangle to be marked, and its width
            and height.

        inset_ax : `.Axes`
            An optional inset Axes to draw connecting lines to.  Two lines are
            drawn connecting the indicator box to the inset Axes on corners
            chosen so as to not overlap with the indicator box.

        transform : `.Transform`
            Transform for the rectangle coordinates. Defaults to
            `ax.transAxes`, i.e. the units of *rect* are in Axes-relative
            coordinates.

        facecolor : color, default: 'none'
            Facecolor of the rectangle.

        edgecolor : color, default: '0.5'
            Color of the rectangle and color of the connecting lines.

        alpha : float, default: 0.5
            Transparency of the rectangle and connector lines.

        zorder : float, default: 4.99
            Drawing order of the rectangle and connector lines.  The default,
            4.99, is just below the default level of inset Axes.

        **kwargs
            Other keyword arguments are passed on to the `.Rectangle` patch:

            %(Rectangle:kwdoc)s

        Returns
        -------
        rectangle_patch : `.patches.Rectangle`
             The indicator frame.

        connector_lines : 4-tuple of `.patches.ConnectionPatch`
            The four connector lines connecting to (lower_left, upper_left,
            lower_right upper_right) corners of *inset_ax*. Two lines are
            set with visibility to *False*,  but the user can set the
            visibility to True if the automatic choice is not deemed correct.

        """
        # to make the axes connectors work, we need to apply the aspect to
        # the parent axes.
        self.apply_aspect()

        if transform is None:
            transform = self.transData
        kwargs.setdefault('label', '_indicate_inset')

        x, y, width, height = bounds
        rectangle_patch = mpatches.Rectangle(
            (x, y), width, height,
            facecolor=facecolor, edgecolor=edgecolor, alpha=alpha,
            zorder=zorder, transform=transform, **kwargs)
        self.add_patch(rectangle_patch)

        connects = []

        if inset_ax is not None:
            # connect the inset_axes to the rectangle
            for xy_inset_ax in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                # inset_ax positions are in axes coordinates
                # The 0, 1 values define the four edges if the inset_ax
                # lower_left, upper_left, lower_right upper_right.
                ex, ey = xy_inset_ax
                if self.xaxis.get_inverted():
                    ex = 1 - ex
                if self.yaxis.get_inverted():
                    ey = 1 - ey
                xy_data = x + ex * width, y + ey * height
                p = mpatches.ConnectionPatch(
                    xyA=xy_inset_ax, coordsA=inset_ax.transAxes,
                    xyB=xy_data, coordsB=self.transData,
                    arrowstyle="-", zorder=zorder,
                    edgecolor=edgecolor, alpha=alpha)
                connects.append(p)
                self.add_patch(p)

            # decide which two of the lines to keep visible....
            pos = inset_ax.get_position()
            bboxins = pos.transformed(self.figure.transSubfigure)
            rectbbox = mtransforms.Bbox.from_bounds(
                *bounds
            ).transformed(transform)
            x0 = rectbbox.x0 < bboxins.x0
            x1 = rectbbox.x1 < bboxins.x1
            y0 = rectbbox.y0 < bboxins.y0
            y1 = rectbbox.y1 < bboxins.y1
            connects[0].set_visible(x0 ^ y0)
            connects[1].set_visible(x0 == y1)
            connects[2].set_visible(x1 == y0)
            connects[3].set_visible(x1 ^ y1)

        return rectangle_patch, tuple(connects) if connects else None

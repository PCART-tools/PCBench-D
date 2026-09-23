    def indicate_inset(self, bounds, inset_ax=None, *, transform=None,
            facecolor='none', edgecolor='0.5', alpha=0.5,
            zorder=4.99, **kwargs):
        """
        Add an inset indicator to the axes.  This is a rectangle on the plot
        at the position indicated by *bounds* that optionally has lines that
        connect the rectangle to an inset axes
        (`.Axes.inset_axes`).

        Warnings
        --------

        This method is experimental as of 3.0, and the API may change.


        Parameters
        ----------

        bounds : [x0, y0, width, height]
            Lower-left corner of rectangle to be marked, and its width
            and height.

        inset_ax : `.Axes`
            An optional inset axes to draw connecting lines to.  Two lines are
            drawn connecting the indicator box to the inset axes on corners
            chosen so as to not overlap with the indicator box.

        transform : `.Transform`
            Transform for the rectangle co-ordinates. Defaults to
            `ax.transAxes`, i.e. the units of *rect* are in axes-relative
            coordinates.

        facecolor : Matplotlib color
            Facecolor of the rectangle (default 'none').

        edgecolor : Matplotlib color
            Color of the rectangle and color of the connecting lines.  Default
            is '0.5'.

        alpha : number
            Transparency of the rectangle and connector lines.  Default is 0.5.

        zorder : number
            Drawing order of the rectangle and connector lines. Default is 4.99
            (just below the default level of inset axes).

        **kwargs
            Other *kwargs* are passed on to the rectangle patch.

        Returns
        -------

        rectangle_patch : `.Patches.Rectangle`
             Rectangle artist.

        connector_lines : 4-tuple of `.Patches.ConnectionPatch`
            One for each of four connector lines.  Two are set with visibility
            to *False*,  but the user can set the visibility to True if the
            automatic choice is not deemed correct.

        """

        # to make the axes connectors work, we need to apply the aspect to
        # the parent axes.
        self.apply_aspect()

        if transform is None:
            transform = self.transData
        label = kwargs.pop('label', 'indicate_inset')

        xy = (bounds[0], bounds[1])
        rectpatch = mpatches.Rectangle(xy, bounds[2], bounds[3],
                facecolor=facecolor, edgecolor=edgecolor, alpha=alpha,
                zorder=zorder,  label=label, transform=transform, **kwargs)
        self.add_patch(rectpatch)

        if inset_ax is not None:
            # want to connect the indicator to the rect....
            connects = []
            xr = [bounds[0], bounds[0]+bounds[2]]
            yr = [bounds[1], bounds[1]+bounds[3]]
            for xc in range(2):
                for yc in range(2):
                    xyA = (xc, yc)
                    xyB = (xr[xc], yr[yc])
                    connects += [mpatches.ConnectionPatch(xyA, xyB,
                            'axes fraction', 'data',
                            axesA=inset_ax, axesB=self, arrowstyle="-",
                            zorder=zorder, edgecolor=edgecolor, alpha=alpha)]
                    self.add_patch(connects[-1])
            # decide which two of the lines to keep visible....
            pos = inset_ax.get_position()
            bboxins = pos.transformed(self.figure.transFigure)
            rectbbox = mtransforms.Bbox.from_bounds(
                        *bounds).transformed(transform)
            x0 = rectbbox.x0 < bboxins.x0
            x1 = rectbbox.x1 < bboxins.x1
            y0 = rectbbox.y0 < bboxins.y0
            y1 = rectbbox.y1 < bboxins.y1
            connects[0].set_visible(x0 ^ y0)
            connects[1].set_visible(x0 == y1)
            connects[2].set_visible(x1 == y0)
            connects[3].set_visible(x1 ^ y1)

        return rectpatch, connects

    def inset_axes(self, bounds, *, transform=None, zorder=5,
            **kwargs):
        """
        Add a child inset axes to this existing axes.

        Warnings
        --------

        This method is experimental as of 3.0, and the API may change.

        Parameters
        ----------

        bounds : [x0, y0, width, height]
            Lower-left corner of inset axes, and its width and height.

        transform : `.Transform`
            Defaults to `ax.transAxes`, i.e. the units of *rect* are in
            axes-relative coordinates.

        zorder : number
            Defaults to 5 (same as `.Axes.legend`).  Adjust higher or lower
            to change whether it is above or below data plotted on the
            parent axes.

        **kwargs

            Other *kwargs* are passed on to the `axes.Axes` child axes.

        Returns
        -------

        Axes
            The created `.axes.Axes` instance.

        Examples
        --------

        This example makes two inset axes, the first is in axes-relative
        coordinates, and the second in data-coordinates::

            fig, ax = plt.subplots()
            ax.plot(range(10))
            axin1 = ax.inset_axes([0.8, 0.1, 0.15, 0.15])
            axin2 = ax.inset_axes(
                    [5, 7, 2.3, 2.3], transform=ax.transData)

        """
        if transform is None:
            transform = self.transAxes
        label = kwargs.pop('label', 'inset_axes')

        # This puts the rectangle into figure-relative coordinates.
        inset_locator = _make_inset_locator(bounds, transform, self)
        bb = inset_locator(None, None)

        inset_ax = Axes(self.figure, bb.bounds, zorder=zorder,
                label=label, **kwargs)

        # this locator lets the axes move if in data coordinates.
        # it gets called in `ax.apply_aspect() (of all places)
        inset_ax.set_axes_locator(inset_locator)

        self.add_child_axes(inset_ax)

        return inset_ax

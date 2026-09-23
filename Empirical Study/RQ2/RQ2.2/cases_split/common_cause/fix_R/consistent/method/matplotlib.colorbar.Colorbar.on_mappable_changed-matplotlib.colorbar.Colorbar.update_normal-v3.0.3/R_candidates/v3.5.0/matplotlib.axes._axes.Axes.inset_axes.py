    def inset_axes(self, bounds, *, transform=None, zorder=5, **kwargs):
        """
        Add a child inset Axes to this existing Axes.

        Warnings
        --------
        This method is experimental as of 3.0, and the API may change.

        Parameters
        ----------
        bounds : [x0, y0, width, height]
            Lower-left corner of inset Axes, and its width and height.

        transform : `.Transform`
            Defaults to `ax.transAxes`, i.e. the units of *rect* are in
            Axes-relative coordinates.

        zorder : number
            Defaults to 5 (same as `.Axes.legend`).  Adjust higher or lower
            to change whether it is above or below data plotted on the
            parent Axes.

        **kwargs
            Other keyword arguments are passed on to the child `.Axes`.

        Returns
        -------
        ax
            The created `~.axes.Axes` instance.

        Examples
        --------
        This example makes two inset Axes, the first is in Axes-relative
        coordinates, and the second in data-coordinates::

            fig, ax = plt.subplots()
            ax.plot(range(10))
            axin1 = ax.inset_axes([0.8, 0.1, 0.15, 0.15])
            axin2 = ax.inset_axes(
                    [5, 7, 2.3, 2.3], transform=ax.transData)

        """
        if transform is None:
            transform = self.transAxes
        kwargs.setdefault('label', 'inset_axes')

        # This puts the rectangle into figure-relative coordinates.
        inset_locator = _TransformedBoundsLocator(bounds, transform)
        bounds = inset_locator(self, None).bounds
        inset_ax = Axes(self.figure, bounds, zorder=zorder, **kwargs)
        # this locator lets the axes move if in data coordinates.
        # it gets called in `ax.apply_aspect() (of all places)
        inset_ax.set_axes_locator(inset_locator)

        self.add_child_axes(inset_ax)

        return inset_ax

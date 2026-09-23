    @_preprocess_data(replace_names=["x", "y"], label_namer=None,
                      positional_parameter_names=["x", "y", "c"])
    def fill(self, *args, **kwargs):
        """
        Plot filled polygons.

        Parameters
        ----------
        args : a variable length argument
            It allowing for multiple
            *x*, *y* pairs with an optional color format string; see
            :func:`~matplotlib.pyplot.plot` for details on the argument
            parsing.  For example, each of the following is legal::

                ax.fill(x, y)
                ax.fill(x, y, "b")
                ax.fill(x, y, "b", x, y, "r")

            An arbitrary number of *x*, *y*, *color* groups can be specified::
            ax.fill(x1, y1, 'g', x2, y2, 'r')

        Returns
        -------
        a list of :class:`~matplotlib.patches.Patch`

        Other Parameters
        ----------------
        **kwargs : :class:`~matplotlib.patches.Polygon` properties

        Notes
        -----
        The same color strings that :func:`~matplotlib.pyplot.plot`
        supports are supported by the fill format string.

        If you would like to fill below a curve, e.g., shade a region
        between 0 and *y* along *x*, use :meth:`fill_between`


        """
        if not self._hold:
            self.cla()

        kwargs = cbook.normalize_kwargs(kwargs, _alias_map)

        patches = []
        for poly in self._get_patches_for_fill(*args, **kwargs):
            self.add_patch(poly)
            patches.append(poly)
        self.autoscale_view()
        return patches

    @_preprocess_data(replace_names=["x", "y"], label_namer=None,
                      positional_parameter_names=["x", "y", "c"])
    def fill(self, *args, **kwargs):
        """
        Plot filled polygons.

        Parameters
        ----------
        args : sequence of x, y, [color]
            Each polygon is defined by the lists of *x* and *y* positions of
            its nodes, optionally followed by a *color* specifier. See
            :mod:`matplotlib.colors` for supported color specifiers. The
            standard color cycle is used for polygons without a color
            specifier.

            You can plot multiple polygons by providing multiple *x*, *y*,
            *[color]* groups.

            For example, each of the following is legal::

                ax.fill(x, y)                    # a polygon with default color
                ax.fill(x, y, "b")               # a blue polygon
                ax.fill(x, y, x2, y2)            # two polygons
                ax.fill(x, y, "b", x2, y2, "r")  # a blue and a red polygon

        Returns
        -------
        a list of :class:`~matplotlib.patches.Polygon`

        Other Parameters
        ----------------
        **kwargs : :class:`~matplotlib.patches.Polygon` properties

        Notes
        -----
        Use :meth:`fill_between` if you would like to fill the region between
        two curves.
        """
        # For compatibility(!), get aliases from Line2D rather than Patch.
        kwargs = cbook.normalize_kwargs(kwargs, mlines.Line2D._alias_map)

        patches = []
        for poly in self._get_patches_for_fill(*args, **kwargs):
            self.add_patch(poly)
            patches.append(poly)
        self.autoscale_view()
        return patches

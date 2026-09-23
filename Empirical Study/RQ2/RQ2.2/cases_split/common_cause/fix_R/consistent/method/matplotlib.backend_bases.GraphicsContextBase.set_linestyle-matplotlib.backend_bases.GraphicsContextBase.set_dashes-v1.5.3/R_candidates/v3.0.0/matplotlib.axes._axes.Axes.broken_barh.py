    @_preprocess_data(label_namer=None)
    @docstring.dedent_interpd
    def broken_barh(self, xranges, yrange, **kwargs):
        """
        Plot a horizontal sequence of rectangles.

        A rectangle is drawn for each element of *xranges*. All rectangles
        have the same vertical position and size defined by *yrange*.

        This is a convenience function for instantiating a
        `.BrokenBarHCollection`, adding it to the axes and autoscaling the
        view.

        Parameters
        ----------
        xranges : sequence of tuples (*xmin*, *xwidth*)
            The x-positions and extends of the rectangles. For each tuple
            (*xmin*, *xwidth*) a rectangle is drawn from *xmin* to *xmin* +
            *xwidth*.
        yranges : (*ymin*, *ymax*)
            The y-position and extend for all the rectangles.

        Other Parameters
        ----------------
        **kwargs : :class:`.BrokenBarHCollection` properties

            Each *kwarg* can be either a single argument applying to all
            rectangles, e.g.::

                facecolors='black'

            or a sequence of arguments over which is cycled, e.g.::

                facecolors=('black', 'blue')

            would create interleaving black and blue rectangles.

            Supported keywords:

            %(BrokenBarHCollection)s

        Returns
        -------
        collection : A :class:`~.collections.BrokenBarHCollection`

        Notes
        -----
        .. [Notes section required for data comment. See #10189.]

        """
        # process the unit information
        if len(xranges):
            xdata = cbook.safe_first_element(xranges)
        else:
            xdata = None
        if len(yrange):
            ydata = cbook.safe_first_element(yrange)
        else:
            ydata = None
        self._process_unit_info(xdata=xdata,
                                ydata=ydata,
                                kwargs=kwargs)
        xranges = self.convert_xunits(xranges)
        yrange = self.convert_yunits(yrange)

        col = mcoll.BrokenBarHCollection(xranges, yrange, **kwargs)
        self.add_collection(col, autolim=True)
        self.autoscale_view()

        return col

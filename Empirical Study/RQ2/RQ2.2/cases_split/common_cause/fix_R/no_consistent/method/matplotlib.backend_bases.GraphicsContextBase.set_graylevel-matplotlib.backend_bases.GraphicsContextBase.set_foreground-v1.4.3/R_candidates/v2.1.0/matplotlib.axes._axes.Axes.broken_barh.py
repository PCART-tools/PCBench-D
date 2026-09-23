    @_preprocess_data(label_namer=None)
    @docstring.dedent_interpd
    def broken_barh(self, xranges, yrange, **kwargs):
        """
        Plot horizontal bars.

        A collection of horizontal bars spanning *yrange* with a sequence of
        *xranges*.

        Required arguments:

          =========   ==============================
          Argument    Description
          =========   ==============================
          *xranges*   sequence of (*xmin*, *xwidth*)
          *yrange*    sequence of (*ymin*, *ywidth*)
          =========   ==============================

        kwargs are
        :class:`matplotlib.collections.BrokenBarHCollection`
        properties:

        %(BrokenBarHCollection)s

        these can either be a single argument, i.e.,::

          facecolors = 'black'

        or a sequence of arguments for the various bars, i.e.,::

          facecolors = ('black', 'red', 'green')
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

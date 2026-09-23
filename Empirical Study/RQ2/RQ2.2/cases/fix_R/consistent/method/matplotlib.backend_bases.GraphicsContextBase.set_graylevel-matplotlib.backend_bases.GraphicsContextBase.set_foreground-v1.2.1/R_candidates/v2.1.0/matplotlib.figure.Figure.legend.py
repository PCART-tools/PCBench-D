    def legend(self, *args, **kwargs):
        """
        Place a legend on the figure.

        To make a legend from existing artists on every axes::

          legend()

        To make a legend for a list of lines and labels::

          legend( (line1, line2, line3),
                  ('label1', 'label2', 'label3'),
                  'upper right')

        Parameters
        ----------
        loc : string or integer
            The location of the legend. Possible codes are:

                ===============   =============
                Location String   Location Code
                ===============   =============
                'upper right'     1
                'upper left'      2
                'lower left'      3
                'lower right'     4
                'right'           5
                'center left'     6
                'center right'    7
                'lower center'    8
                'upper center'    9
                'center'          10
                ===============   =============

            *loc* can also be an (x,y) tuple in figure coords, which specifies
            the lower left of the legend box. In figure coords (0,0) is the
            bottom left of the figure, and (1,1) is the top right.

        prop : None or FontProperties or dict
            A :class:`matplotlib.font_manager.FontProperties` instance. If
            *prop* is a dictionary, a new instance will be created with *prop*.
            If *None*, use rc settings.

        numpoints : integer
            The number of points in the legend line, default is 4

        scatterpoints : integer
            The number of points in the legend line, default is 4

        scatteryoffsets : list of floats
            A list of yoffsets for scatter symbols in legend

        markerscale : None or scalar
            The relative size of legend markers vs. original. If *None*, use rc
            settings.

        markerfirst : bool
            If *True*, legend marker is placed to the left of the legend label.
            If *False*, legend marker is placed to the right of the legend
            label.
            Default is *True*.

        frameon : None or bool
            Control whether the legend should be drawn on a patch (frame).
            Default is *None* which will take the value from the
            ``legend.frameon`` :data:`rcParam<matplotlib.rcParams>`.

        fancybox : None or bool
            If *True*, draw a frame with a round fancybox. If *None*, use rc
            settings.

        shadow : None or bool
            If *True*, draw a shadow behind legend. If *None*, use rc settings.

        framealpha : None or float
            Control the alpha transparency of the legend's background.
            Default is *None* which will take the value from the
            ``legend.framealpha`` :data:`rcParam<matplotlib.rcParams>`.

        facecolor : None or "inherit" or a color spec
            Control the legend's background color.
            Default is *None* which will take the value from the
            ``legend.facecolor`` :data:`rcParam<matplotlib.rcParams>`.
            If ``"inherit"``, it will take the ``axes.facecolor``
            :data:`rcParam<matplotlib.rcParams>`.

        edgecolor : None or "inherit" or a color spec
            Control the legend's background patch edge color.
            Default is *None* which will take the value from the
            ``legend.edgecolor`` :data:`rcParam<matplotlib.rcParams>`.
            If ``"inherit"``, it will take the ``axes.edgecolor``
            :data:`rcParam<matplotlib.rcParams>`.

        ncol : integer
            Number of columns. Default is 1.

        mode : "expand" or None
            If mode is "expand", the legend will be horizontally expanded
            to fill the axes area (or *bbox_to_anchor*)

        title : string
            The legend title

        borderpad : float or None
            The fractional whitespace inside the legend border, measured in
            font-size units.
            Default is *None* which will take the value from the
            ``legend.borderpad`` :data:`rcParam<matplotlib.rcParams>`.

        labelspacing : float or None
            The vertical space between the legend entries, measured in
            font-size units.
            Default is *None* which will take the value from the
            ``legend.labelspacing`` :data:`rcParam<matplotlib.rcParams>`.

        handlelength : float or None
            The length of the legend handles, measured in font-size units.
            Default is *None* which will take the value from the
            ``legend.handlelength`` :data:`rcParam<matplotlib.rcParams>`.

        handletextpad : float or None
            The padding between the legend handle and text, measured in
            font-size units.
            Default is *None* which will take the value from the
            ``legend.handletextpad`` :data:`rcParam<matplotlib.rcParams>`.

        borderaxespad : float or None
            The padding between the axes and legend border, measured in
            font-size units.
            Default is *None* which will take the value from the
            ``legend.borderaxespad`` :data:`rcParam<matplotlib.rcParams>`.

        columnspacing : float or None
            The spacing between columns, measured in font-size units.
            Default is *None* which will take the value from the
            ``legend.columnspacing`` :data:`rcParam<matplotlib.rcParams>`.

        Returns
        -------
        :class:`matplotlib.legend.Legend` instance

        Notes
        -----
        Not all kinds of artist are supported by the legend command. See
        :ref:`sphx_glr_tutorials_intermediate_legend_guide.py` for details.
        """

        # If no arguments given, collect up all the artists on the figure
        if len(args) == 0:
            handles = []
            labels = []

            def in_handles(h, l):
                # Method to check if we already have a given handle and label.
                # Consider two handles to be the same if they share a label,
                # color, facecolor, and edgecolor.

                # Loop through each handle and label already collected
                for f_h, f_l in zip(handles, labels):
                    if f_l != l:
                        continue
                    if type(f_h) != type(h):
                        continue
                    try:
                        if f_h.get_color() != h.get_color():
                            continue
                    except AttributeError:
                        pass
                    try:
                        if f_h.get_facecolor() != h.get_facecolor():
                            continue
                    except AttributeError:
                        pass
                    try:
                        if f_h.get_edgecolor() != h.get_edgecolor():
                            continue
                    except AttributeError:
                        pass
                    return True
                return False

            for ax in self.axes:
                ax_handles, ax_labels = ax.get_legend_handles_labels()
                for h, l in zip(ax_handles, ax_labels):
                    if not in_handles(h, l):
                        handles.append(h)
                        labels.append(l)
            if len(handles) == 0:
                warnings.warn("No labeled objects found. "
                              "Use label='...' kwarg on individual plots.")
                return None

        elif len(args) == 2:
            # LINES, LABELS
            handles, labels = args

        elif len(args) == 3:
            # LINES, LABELS, LOC
            handles, labels, loc = args
            kwargs['loc'] = loc

        else:
            raise TypeError('Invalid number of arguments passed to legend. '
                            'Please specify either 0 args, 2 args '
                            '(artist handles, figure labels) or 3 args '
                            '(artist handles, figure labels, legend location)')

        l = Legend(self, handles, labels, **kwargs)
        self.legends.append(l)
        l._remove_method = lambda h: self.legends.remove(h)
        self.stale = True
        return l

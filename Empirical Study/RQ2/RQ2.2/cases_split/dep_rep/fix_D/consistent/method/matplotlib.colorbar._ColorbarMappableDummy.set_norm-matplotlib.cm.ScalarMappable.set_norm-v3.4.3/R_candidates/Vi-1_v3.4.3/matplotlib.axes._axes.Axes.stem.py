    @_preprocess_data()
    def stem(self, *args, linefmt=None, markerfmt=None, basefmt=None, bottom=0,
             label=None, use_line_collection=True, orientation='vertical'):
        """
        Create a stem plot.

        A stem plot draws lines perpendicular to a baseline at each location
        *locs* from the baseline to *heads*, and places a marker there. For
        vertical stem plots (the default), the *locs* are *x* positions, and
        the *heads* are *y* values. For horizontal stem plots, the *locs* are
        *y* positions, and the *heads* are *x* values.

        Call signature::

          stem([locs,] heads, linefmt=None, markerfmt=None, basefmt=None)

        The *locs*-positions are optional. The formats may be provided either
        as positional or as keyword-arguments.

        Parameters
        ----------
        locs : array-like, default: (0, 1, ..., len(heads) - 1)
            For vertical stem plots, the x-positions of the stems.
            For horizontal stem plots, the y-positions of the stems.

        heads : array-like
            For vertical stem plots, the y-values of the stem heads.
            For horizontal stem plots, the x-values of the stem heads.

        linefmt : str, optional
            A string defining the color and/or linestyle of the vertical lines:

            =========  =============
            Character  Line Style
            =========  =============
            ``'-'``    solid line
            ``'--'``   dashed line
            ``'-.'``   dash-dot line
            ``':'``    dotted line
            =========  =============

            Default: 'C0-', i.e. solid line with the first color of the color
            cycle.

            Note: Markers specified through this parameter (e.g. 'x') will be
            silently ignored (unless using ``use_line_collection=False``).
            Instead, markers should be specified using *markerfmt*.

        markerfmt : str, optional
            A string defining the color and/or shape of the markers at the stem
            heads.  Default: 'C0o', i.e. filled circles with the first color of
            the color cycle.

        basefmt : str, default: 'C3-' ('C2-' in classic mode)
            A format string defining the properties of the baseline.

        orientation : str, default: 'vertical'
            If 'vertical', will produce a plot with stems oriented vertically,
            otherwise the stems will be oriented horizontally.

        bottom : float, default: 0
            The y/x-position of the baseline (depending on orientation).

        label : str, default: None
            The label to use for the stems in legends.

        use_line_collection : bool, default: True
            If ``True``, store and plot the stem lines as a
            `~.collections.LineCollection` instead of individual lines, which
            significantly increases performance.  If ``False``, defaults to the
            old behavior of using a list of `.Line2D` objects.  This parameter
            may be deprecated in the future.

        Returns
        -------
        `.StemContainer`
            The container may be treated like a tuple
            (*markerline*, *stemlines*, *baseline*)

        Notes
        -----
        .. seealso::
            The MATLAB function
            `stem <https://www.mathworks.com/help/matlab/ref/stem.html>`_
            which inspired this method.
        """
        if not 1 <= len(args) <= 5:
            raise TypeError('stem expected between 1 and 5 positional '
                            'arguments, got {}'.format(args))
        _api.check_in_list(['horizontal', 'vertical'], orientation=orientation)

        if len(args) == 1:
            heads, = args
            locs = np.arange(len(heads))
            args = ()
        else:
            locs, heads, *args = args

        if orientation == 'vertical':
            locs, heads = self._process_unit_info([("x", locs), ("y", heads)])
        else:
            heads, locs = self._process_unit_info([("x", heads), ("y", locs)])

        # defaults for formats
        if linefmt is None:
            try:
                # fallback to positional argument
                linefmt = args[0]
            except IndexError:
                linecolor = 'C0'
                linemarker = 'None'
                linestyle = '-'
            else:
                linestyle, linemarker, linecolor = \
                    _process_plot_format(linefmt)
        else:
            linestyle, linemarker, linecolor = _process_plot_format(linefmt)

        if markerfmt is None:
            try:
                # fallback to positional argument
                markerfmt = args[1]
            except IndexError:
                markercolor = 'C0'
                markermarker = 'o'
                markerstyle = 'None'
            else:
                markerstyle, markermarker, markercolor = \
                    _process_plot_format(markerfmt)
        else:
            markerstyle, markermarker, markercolor = \
                _process_plot_format(markerfmt)

        if basefmt is None:
            try:
                # fallback to positional argument
                basefmt = args[2]
            except IndexError:
                if rcParams['_internal.classic_mode']:
                    basecolor = 'C2'
                else:
                    basecolor = 'C3'
                basemarker = 'None'
                basestyle = '-'
            else:
                basestyle, basemarker, basecolor = \
                    _process_plot_format(basefmt)
        else:
            basestyle, basemarker, basecolor = _process_plot_format(basefmt)

        # New behaviour in 3.1 is to use a LineCollection for the stemlines
        if use_line_collection:
            if linestyle is None:
                linestyle = rcParams['lines.linestyle']
            xlines = self.vlines if orientation == "vertical" else self.hlines
            stemlines = xlines(
                locs, bottom, heads,
                colors=linecolor, linestyles=linestyle, label="_nolegend_")
        # Old behaviour is to plot each of the lines individually
        else:
            stemlines = []
            for loc, head in zip(locs, heads):
                if orientation == 'horizontal':
                    xs = [bottom, head]
                    ys = [loc, loc]
                else:
                    xs = [loc, loc]
                    ys = [bottom, head]
                l, = self.plot(xs, ys,
                               color=linecolor, linestyle=linestyle,
                               marker=linemarker, label="_nolegend_")
                stemlines.append(l)

        if orientation == 'horizontal':
            marker_x = heads
            marker_y = locs
            baseline_x = [bottom, bottom]
            baseline_y = [np.min(locs), np.max(locs)]
        else:
            marker_x = locs
            marker_y = heads
            baseline_x = [np.min(locs), np.max(locs)]
            baseline_y = [bottom, bottom]

        markerline, = self.plot(marker_x, marker_y,
                                color=markercolor, linestyle=markerstyle,
                                marker=markermarker, label="_nolegend_")

        baseline, = self.plot(baseline_x, baseline_y,
                              color=basecolor, linestyle=basestyle,
                              marker=basemarker, label="_nolegend_")

        stem_container = StemContainer((markerline, stemlines, baseline),
                                       label=label)
        self.add_container(stem_container)
        return stem_container

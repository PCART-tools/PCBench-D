    @_preprocess_data(replace_all_args=True, label_namer=None)
    def stem(self, *args, linefmt=None, markerfmt=None, basefmt=None,
             bottom=0, label=None):
        """
        Create a stem plot.

        A stem plot plots vertical lines at each *x* location from the baseline
        to *y*, and places a marker there.

        Call signature::

          stem([x,] y, linefmt=None, markerfmt=None, basefmt=None)

        The x-positions are optional. The formats may be provided either as
        positional or as keyword-arguments.

        Parameters
        ----------
        x : array-like, optional
            The x-positions of the stems. Default: (0, 1, ..., len(y) - 1).

        y : array-like
            The y-values of the stem heads.

        linefmt : str, optional
            A string defining the properties of the vertical lines. Usually,
            this will be a color or a color and a linestyle:

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

            Note: While it is technically possible to specify valid formats
            other than color or color and linestyle (e.g. 'rx' or '-.'), this
            is beyond the intention of the method and will most likely not
            result in a reasonable reasonable plot.

        markerfmt : str, optional
            A string defining the properties of the markers at the stem heads.
            Default: 'C0o', i.e. filled circles with the first color of the
            color cycle.

        basefmt : str, optional
            A format string defining the properties of the baseline.

            Default: 'C3-' ('C2-' in classic mode).

        bottom : float, optional, default: 0
            The y-position of the baseline.

        label : str, optional, default: None
            The label to use for the stems in legends.


        Returns
        -------
        container : :class:`~matplotlib.container.StemContainer`
            The container may be treated like a tuple
            (*markerline*, *stemlines*, *baseline*)


        Notes
        -----

        .. seealso::
            The MATLAB function
            `stem <http://www.mathworks.com/help/techdoc/ref/stem.html>`_
            which inspired this method.

        """
        if not 1 <= len(args) <= 5:
            raise TypeError('stem expected between 1 and 5 positional '
                            'arguments, got {}'.format(args))

        y = np.asarray(args[0])
        args = args[1:]

        # Try a second one
        if not args:
            x = np.arange(len(y))
        else:
            x = y
            y = np.asarray(args[0], dtype=float)
            args = args[1:]

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

        markerline, = self.plot(x, y, color=markercolor, linestyle=markerstyle,
                                marker=markermarker, label="_nolegend_")

        stemlines = []
        for thisx, thisy in zip(x, y):
            l, = self.plot([thisx, thisx], [bottom, thisy],
                           color=linecolor, linestyle=linestyle,
                           marker=linemarker, label="_nolegend_")
            stemlines.append(l)

        baseline, = self.plot([np.min(x), np.max(x)], [bottom, bottom],
                              color=basecolor, linestyle=basestyle,
                              marker=basemarker, label="_nolegend_")

        stem_container = StemContainer((markerline, stemlines, baseline),
                                       label=label)
        self.add_container(stem_container)

        return stem_container
